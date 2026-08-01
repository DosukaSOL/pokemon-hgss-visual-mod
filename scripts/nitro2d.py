#!/usr/bin/env python3
"""Minimal NCLR/NCGR/NSCR codec for boot-screen editing.

Supports 4bpp/8bpp tiled backgrounds with tilemap (NSCR) rendering and
re-encoding. Only the features needed by this project are implemented.
"""
from __future__ import annotations

import struct

import ndspy.lz10


def maybe_decompress(data: bytes) -> tuple[bytes, bool]:
    if data[:1] == b"\x10":
        try:
            return bytes(ndspy.lz10.decompress(data)), True
        except Exception:
            pass
    return bytes(data), False


def _first_section(data: bytes, magic: bytes) -> int:
    off = data.find(magic)
    if off == -1:
        raise ValueError(f"section {magic!r} not found")
    return off


class NCLR:
    def __init__(self, data: bytes):
        self.raw, self.compressed = maybe_decompress(data)
        off = _first_section(self.raw, b"TTLP")
        (self.fmt,) = struct.unpack_from("<I", self.raw, off + 8)
        (data_size,) = struct.unpack_from("<I", self.raw, off + 16)
        (pal_off,) = struct.unpack_from("<I", self.raw, off + 20)
        base = off + 8 + 16 + pal_off
        n = min(data_size, len(self.raw) - base) // 2
        self.colors = []
        for i in range(n):
            (v,) = struct.unpack_from("<H", self.raw, base + i * 2)
            r = (v & 31) << 3
            g = ((v >> 5) & 31) << 3
            b = ((v >> 10) & 31) << 3
            self.colors.append((r, g, b))


class NCGR:
    def __init__(self, data: bytes):
        self.raw, self.compressed = maybe_decompress(data)
        self.char_off = _first_section(self.raw, b"RAHC")
        (self.h_tiles, self.w_tiles, self.bitdepth_fmt) = struct.unpack_from(
            "<HHI", self.raw, self.char_off + 8)
        self.is4bpp = self.bitdepth_fmt == 3
        (self.data_size,) = struct.unpack_from("<I", self.raw,
                                               self.char_off + 24)
        (rel,) = struct.unpack_from("<I", self.raw, self.char_off + 28)
        self.data_start = self.char_off + 8 + rel
        self.gfx = bytearray(
            self.raw[self.data_start:self.data_start + self.data_size])

    @property
    def tile_count(self) -> int:
        return len(self.gfx) // (32 if self.is4bpp else 64)

    def tile_pixels(self, idx: int) -> list[int]:
        """64 palette indices for tile idx."""
        if self.is4bpp:
            chunk = self.gfx[idx * 32:(idx + 1) * 32]
            out = []
            for b in chunk:
                out.append(b & 0xF)
                out.append(b >> 4)
            return out
        return list(self.gfx[idx * 64:(idx + 1) * 64])

    def set_tile_pixels(self, idx: int, pixels: list[int]) -> None:
        if self.is4bpp:
            chunk = bytearray()
            for i in range(0, 64, 2):
                chunk.append((pixels[i] & 0xF) | ((pixels[i + 1] & 0xF) << 4))
            self.gfx[idx * 32:(idx + 1) * 32] = chunk
        else:
            self.gfx[idx * 64:(idx + 1) * 64] = bytes(p & 0xFF for p in pixels)

    def append_tiles(self, tiles: list[list[int]]) -> int:
        """Append tiles (each 64 palette indices); returns first new index."""
        first = self.tile_count
        per = 32 if self.is4bpp else 64
        self.gfx.extend(b"\x00" * (per * len(tiles)))
        for i, t in enumerate(tiles):
            self.set_tile_pixels(first + i, t)
        # pad to a whole row so the header tile grid stays integral
        if self.w_tiles not in (0, 0xFFFF):
            rem = self.tile_count % self.w_tiles
            if rem:
                self.gfx.extend(b"\x00" * (per * (self.w_tiles - rem)))
        return first

    def save(self) -> bytes:
        out = bytearray(self.raw[:self.data_start])
        out += self.gfx
        out += self.raw[self.data_start + self.data_size:]
        delta = len(self.gfx) - self.data_size
        if delta:
            struct.pack_into("<I", out, 0x8,
                             struct.unpack_from("<I", self.raw, 0x8)[0] + delta)
            struct.pack_into("<I", out, self.char_off + 4,
                             struct.unpack_from("<I", self.raw,
                                                self.char_off + 4)[0] + delta)
            struct.pack_into("<I", out, self.char_off + 24,
                             self.data_size + delta)
            if self.w_tiles not in (0, 0xFFFF):
                struct.pack_into("<H", out, self.char_off + 8,
                                 len(self.gfx) // (32 if self.is4bpp else 64)
                                 // self.w_tiles)
        return bytes(out)


class NSCR:
    def __init__(self, data: bytes):
        self.raw, self.compressed = maybe_decompress(data)
        off = _first_section(self.raw, b"NRCS")
        (self.width, self.height, self.fmt, self.map_size) = struct.unpack_from(
            "<HHII", self.raw, off + 8)
        self.map_start = off + 20
        self.entries = list(struct.unpack_from(
            f"<{self.map_size // 2}H", self.raw, self.map_start))

    def entry(self, tx: int, ty: int) -> tuple[int, bool, bool, int]:
        e = self.entries[ty * (self.width // 8) + tx]
        return e & 0x3FF, bool(e & 0x400), bool(e & 0x800), e >> 12

    def set_entry(self, tx: int, ty: int, tile: int, hflip=False,
                  vflip=False, pal: int = 0) -> None:
        e = (tile & 0x3FF) | (hflip << 10) | (vflip << 11) | (pal << 12)
        self.entries[ty * (self.width // 8) + tx] = e

    def save(self) -> bytes:
        out = bytearray(self.raw)
        struct.pack_into(f"<{len(self.entries)}H", out, self.map_start,
                         *self.entries)
        return bytes(out)


def render(nscr: NSCR, ncgr: NCGR, nclr: NCLR):
    """Render to a PIL Image (RGB)."""
    from PIL import Image
    img = Image.new("RGB", (nscr.width, nscr.height))
    px = img.load()
    for ty in range(nscr.height // 8):
        for tx in range(nscr.width // 8):
            tile, hf, vf, pal = nscr.entry(tx, ty)
            if tile >= ncgr.tile_count:
                continue
            pixels = ncgr.tile_pixels(tile)
            for py in range(8):
                for pxi in range(8):
                    sx = 7 - pxi if hf else pxi
                    sy = 7 - py if vf else py
                    idx = pixels[sy * 8 + sx]
                    ci = (pal * 16 + idx) if ncgr.is4bpp else idx
                    color = nclr.colors[ci] if ci < len(nclr.colors) else (255, 0, 255)
                    px[tx * 8 + pxi, ty * 8 + py] = color
    return img
