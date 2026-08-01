#!/usr/bin/env python3
"""Build English Visual+ ROMs and release patches for HeartGold & SoulSilver.

Extracts the Visual+ 1.0.0 components from the Korean HeartGold pair
(clean vs patched) and applies them to the English (USA) ROMs, with
per-site clean-byte verification so nothing is patched blindly.

Components:
  VISUAL  - battle background NARC subfiles (a/0/0/7, a/0/0/8, a/2/6/2),
            arm9 map-header battle-bg IDs (73 entries), arm9 code cave +
            hook (runtime patch of overlay 123), overlay 1 byte @0x277
  HP      - overlay 12 HP-drain speed constants (2 sites, pattern-matched)
  CAMERA  - overlay 1 camera parameter table (full or conservative blend)

Variants:
  visual-only          VISUAL
  safe                 VISUAL + HP
  full                 VISUAL + HP + CAMERA(full)
  conservative-camera  VISUAL + HP + CAMERA(50% blend)

Usage:
    python scripts/port.py [--games heartgold soulsilver] [--variants ...]

ROMs are located via tests/rom_manifest.json hashes; nothing is committed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import ndspy.code
import ndspy.codeCompression as cc
import ndspy.lz10
import ndspy.narc
import ndspy.rom

sys.path.insert(0, str(Path(__file__).resolve().parent))
from profiles import PROFILES, find_rom  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKDIR = REPO_ROOT / "analysis" / "workdir"
RELEASE = REPO_ROOT / "release"

VISUAL_PLUS_VERSION = "1.0.0"

NARC_PATHS = ("a/0/0/7", "a/0/0/8", "a/2/6/2")

# English credit drawn on the boot copyright screen (gs_opening = a/2/6/2;
# NCGR subfile 4 + NSCR subfile 14, both LZ10 — shared by HG and SS)
CREDIT_TEXT = "English Patch By Dosuka"
CREDIT_NARC = "a/2/6/2"
CREDIT_NCGR_IDX = 4
CREDIT_NSCR_IDX = 14
CREDIT_ROW_TY = 21          # empty tilemap rows 20-23, y=168px on screen
CREDIT_COLOR_INDEX = 15     # same greyscale index the existing credits use

# arm9 layout facts established in analysis/ (see hg_kor_full_deep.json)
CAVE_OFFSET = 0x300
CAVE_LEN = 0x2C
HOOK_OFFSET = 0xA18
HOOK_CLEAN = bytes.fromhex("1eff2fe1")          # bx lr
HOOK_MOD = bytes.fromhex("38feffea")            # b cave
NULLPTR_OFFSET = 0xBB4                          # compressed-static-end pointer
MAP_TABLE_DELTA_KOR_TO_USA = -1708              # verified for HG & SS (73/73)
CAVE_LITERAL_KOR = 0x0225F9E0                   # KOR overlay 123 RAM + 0x80
CAVE_LITERAL_USA = 0x0225F0A0                   # USA overlay 123 RAM + 0x80
OV123_SIG = 0xE0095D34

OV1_VISUAL_BYTE = 0x277
CAMERA_TABLE = (0x20B70, 0x20DD0)               # word-aligned scan range, ov1

# overlay 12 HP-drain sites, located by unique byte pattern (region-safe)
HP_SITES = (
    {"pattern": bytes.fromhex("70bd90421dda0002111c"), "target_at": 6,
     "clean": bytes.fromhex("00"), "mod": bytes.fromhex("c0")},
    {"pattern": bytes.fromhex("2860a04207dd2c6005e0808a"), "target_at": 12,
     "clean": bytes.fromhex("081a"), "mod": bytes.fromhex("c81f")},
)

VARIANTS = {
    "visual-only": {"visual": True, "hp": False, "camera": None},
    "safe": {"visual": True, "hp": True, "camera": None},
    "full": {"visual": True, "hp": True, "camera": "full"},
    "conservative-camera": {"visual": True, "hp": True, "camera": "conservative"},
}

GAMES = {
    "heartgold": {"profile": "heartgold_usa", "kor_profile": "heartgold_kor"},
    "soulsilver": {"profile": "soulsilver_usa", "kor_profile": "heartgold_kor"},
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def arm9_decompressed(rom: ndspy.rom.NintendoDSRom) -> bytes:
    data = bytes(rom.arm9)
    try:
        return bytes(cc.decompress(data))
    except Exception:
        return data


def overlay_decompressed(rom: ndspy.rom.NintendoDSRom, oid: int) -> bytes:
    ov = rom.loadArm9Overlays()[oid]
    data = bytes(rom.files[ov.fileID])
    if ov.compressed:
        data = bytes(cc.decompress(data))
    return data


def check(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(f"VERIFICATION FAILED: {msg}")


# ---------------------------------------------------------------- extraction

def add_english_credit(comp: dict) -> None:
    """Draw CREDIT_TEXT under the Korean mod's credits on the boot screen."""
    from PIL import Image, ImageDraw, ImageFont

    from nitro2d import NCGR, NSCR

    edits = comp["narc_edits"][CREDIT_NARC]
    check(CREDIT_NCGR_IDX in edits and CREDIT_NSCR_IDX in edits,
          "boot-screen subfiles not among Visual+ edits")
    g = NCGR(edits[CREDIT_NCGR_IDX]["data"])
    s = NSCR(edits[CREDIT_NSCR_IDX]["data"])

    img = Image.new("1", (256, 16), 0)
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    x0, y0, x1, y1 = draw.textbbox((0, 0), CREDIT_TEXT, font=font)
    draw.text((((256 - (x1 - x0)) // 2) - x0, 2 - y0), CREDIT_TEXT,
              fill=1, font=font)

    px = img.load()
    tiles, mapping = [], []
    for ty in range(2):
        for tx in range(32):
            pixels = [0] * 64
            used = False
            for py in range(8):
                for pxx in range(8):
                    if px[tx * 8 + pxx, ty * 8 + py]:
                        pixels[py * 8 + pxx] = CREDIT_COLOR_INDEX
                        used = True
            if used:
                mapping.append((tx, CREDIT_ROW_TY + ty, len(tiles)))
                tiles.append(pixels)
    check(bool(tiles), "credit text rendered no pixels")
    first = g.append_tiles(tiles)
    for tx, ty, k in mapping:
        check(s.entry(tx, ty)[0] == 0, f"credit target tile ({tx},{ty}) busy")
        s.set_entry(tx, ty, first + k)
    edits[CREDIT_NCGR_IDX]["data"] = ndspy.lz10.compress(g.save())
    edits[CREDIT_NSCR_IDX]["data"] = ndspy.lz10.compress(s.save())


def extract_components(kor_clean: ndspy.rom.NintendoDSRom,
                       kor_mod: ndspy.rom.NintendoDSRom) -> dict:
    comp: dict = {}

    # NARC subfile replacements
    narc_edits: dict[str, dict[int, dict]] = {}
    for path in NARC_PATHS:
        na = ndspy.narc.NARC(bytes(kor_clean.files[kor_clean.filenames.idOf(path)]))
        nb = ndspy.narc.NARC(bytes(kor_mod.files[kor_mod.filenames.idOf(path)]))
        check(len(na.files) == len(nb.files), f"{path} subfile count changed")
        edits = {}
        for i, (fa, fb) in enumerate(zip(na.files, nb.files)):
            if bytes(fa) != bytes(fb):
                edits[i] = {"clean_sha": sha256(bytes(fa)), "data": bytes(fb)}
        narc_edits[path] = edits
    comp["narc_edits"] = narc_edits

    # arm9 map-header battle-bg bytes + cave
    ka, ma = arm9_decompressed(kor_clean), arm9_decompressed(kor_mod)
    check(len(ka) == len(ma), "KOR arm9 size mismatch")
    map_edits = []
    for off in range(len(ka)):
        if ka[off] == ma[off]:
            continue
        if off in (NULLPTR_OFFSET, NULLPTR_OFFSET + 1, NULLPTR_OFFSET + 2,
                   NULLPTR_OFFSET + 3):
            continue
        if CAVE_OFFSET <= off < CAVE_OFFSET + CAVE_LEN:
            continue
        if HOOK_OFFSET <= off < HOOK_OFFSET + 4:
            continue
        map_edits.append({"kor_off": off, "clean": ka[off], "mod": ma[off],
                          "ctx_clean": ka[off - 2:off + 6]})
    check(len(map_edits) == 73, f"expected 73 map edits, got {len(map_edits)}")
    comp["map_edits"] = map_edits
    comp["cave_kor"] = ma[CAVE_OFFSET:CAVE_OFFSET + CAVE_LEN]
    check(ka[HOOK_OFFSET:HOOK_OFFSET + 4] == HOOK_CLEAN, "KOR hook clean bytes")
    check(ma[HOOK_OFFSET:HOOK_OFFSET + 4] == HOOK_MOD, "KOR hook mod bytes")

    # overlay 1: visual byte + camera table words
    k1, m1 = overlay_decompressed(kor_clean, 1), overlay_decompressed(kor_mod, 1)
    comp["ov1_visual"] = {"off": OV1_VISUAL_BYTE,
                          "clean": k1[OV1_VISUAL_BYTE], "mod": m1[OV1_VISUAL_BYTE]}
    cam = []
    for off in range(CAMERA_TABLE[0], CAMERA_TABLE[1], 4):
        a = int.from_bytes(k1[off:off + 4], "little", signed=True)
        b = int.from_bytes(m1[off:off + 4], "little", signed=True)
        if a != b:
            cam.append({"off": off, "clean": a, "mod": b})
    check(len(cam) == 81, f"expected 81 camera words, got {len(cam)}")
    comp["camera_words"] = cam

    # confirm no other ov1 differences outside table + visual byte
    for off in range(len(k1)):
        if k1[off] != m1[off]:
            check(off == OV1_VISUAL_BYTE or
                  CAMERA_TABLE[0] <= off < CAMERA_TABLE[1],
                  f"unexpected ov1 diff at {off:#x}")

    # overlay 12 HP sites: confirm patterns are unique and correct in KOR
    k12, m12 = overlay_decompressed(kor_clean, 12), overlay_decompressed(kor_mod, 12)
    for site in HP_SITES:
        pos = k12.find(site["pattern"])
        check(pos != -1 and k12.find(site["pattern"], pos + 1) == -1,
              "HP pattern not unique in KOR ov12")
        t = pos + site["target_at"]
        check(k12[t:t + len(site["clean"])] == site["clean"], "KOR HP clean bytes")
        check(m12[t:t + len(site["mod"])] == site["mod"], "KOR HP mod bytes")

    add_english_credit(comp)
    return comp


# ------------------------------------------------------------------ applying

def apply_variant(rom: ndspy.rom.NintendoDSRom, comp: dict,
                  variant: str) -> ndspy.rom.NintendoDSRom:
    opts = VARIANTS[variant]
    log: list[str] = []

    if opts["visual"]:
        # NARC subfiles
        for path, edits in comp["narc_edits"].items():
            fid = rom.filenames.idOf(path)
            narc = ndspy.narc.NARC(bytes(rom.files[fid]))
            for i, e in edits.items():
                check(sha256(bytes(narc.files[i])) == e["clean_sha"],
                      f"{path}[{i}] clean subfile differs from KOR baseline")
                narc.files[i] = e["data"]
            rom.files[fid] = narc.save()
            log.append(f"{path}: replaced {len(edits)} subfiles")

        # arm9: decompress, patch, store uncompressed
        a9 = bytearray(arm9_decompressed(rom))
        for e in comp["map_edits"]:
            u = e["kor_off"] + MAP_TABLE_DELTA_KOR_TO_USA
            check(a9[u - 2:u + 6] == e["ctx_clean"],
                  f"map entry mismatch at USA {u:#x}")
            a9[u] = e["mod"]
        cave = bytearray(comp["cave_kor"])
        kor_lit = CAVE_LITERAL_KOR.to_bytes(4, "little")
        check(kor_lit in cave, "KOR literal not in cave")
        idx = cave.index(kor_lit)
        cave[idx:idx + 4] = CAVE_LITERAL_USA.to_bytes(4, "little")
        check(OV123_SIG.to_bytes(4, "little") in cave, "sig literal missing")
        a9[CAVE_OFFSET:CAVE_OFFSET + CAVE_LEN] = cave
        check(bytes(a9[HOOK_OFFSET:HOOK_OFFSET + 4]) == HOOK_CLEAN,
              "USA hook site clean bytes")
        a9[HOOK_OFFSET:HOOK_OFFSET + 4] = HOOK_MOD
        # verify the runtime-patch target exists in USA overlay 123
        ov123 = overlay_decompressed(rom, 123)
        base = CAVE_LITERAL_USA - rom.loadArm9Overlays()[123].ramAddress
        check(int.from_bytes(ov123[base:base + 4], "little") == OV123_SIG,
              "USA ov123 signature mismatch")
        check(ov123[base + 0x8] == 0x73 and ov123[base + 0xC4] == 0x8F,
              "USA ov123 runtime-patch bytes mismatch")
        # null compressed-static-end pointer -> arm9 treated as uncompressed
        check(int.from_bytes(a9[NULLPTR_OFFSET:NULLPTR_OFFSET + 4], "little")
              != 0, "USA nullptr already zero?")
        a9[NULLPTR_OFFSET:NULLPTR_OFFSET + 4] = b"\x00\x00\x00\x00"
        rom.arm9 = bytes(a9)
        log.append(f"arm9: 73 map-header ids, cave@{CAVE_OFFSET:#x}, "
                   f"hook@{HOOK_OFFSET:#x}, stored uncompressed")

    # overlay edits (decompress, patch, recompress, fix table)
    overlays = rom.loadArm9Overlays()

    def write_overlay(oid: int, new_data: bytes) -> None:
        ov = overlays[oid]
        was_compressed = ov.compressed
        ov.data = new_data
        saved = ov.save(compress=was_compressed)
        rom.files[ov.fileID] = saved
        log.append(f"overlay {oid}: rebuilt "
                   f"({'re' if was_compressed else 'un'}compressed, "
                   f"{len(saved)} bytes)")

    if opts["visual"]:
        d1 = bytearray(overlay_decompressed(rom, 1))
        e = comp["ov1_visual"]
        check(d1[e["off"]] == e["clean"], "USA ov1 visual byte mismatch")
        d1[e["off"]] = e["mod"]
        if opts["camera"]:
            blend = 1.0 if opts["camera"] == "full" else 0.5
            for w in comp["camera_words"]:
                cur = int.from_bytes(d1[w["off"]:w["off"] + 4], "little",
                                     signed=True)
                check(cur == w["clean"], f"USA camera word @{w['off']:#x}")
                val = round(w["clean"] + (w["mod"] - w["clean"]) * blend)
                d1[w["off"]:w["off"] + 4] = val.to_bytes(4, "little",
                                                         signed=True)
            log.append(f"camera: {len(comp['camera_words'])} words, "
                       f"blend={blend}")
        write_overlay(1, bytes(d1))

    if opts["hp"]:
        d12 = bytearray(overlay_decompressed(rom, 12))
        for site in HP_SITES:
            pos = bytes(d12).find(site["pattern"])
            check(pos != -1 and bytes(d12).find(site["pattern"], pos + 1) == -1,
                  "HP pattern not unique in USA ov12")
            t = pos + site["target_at"]
            check(bytes(d12[t:t + len(site["clean"])]) == site["clean"],
                  "USA HP clean bytes mismatch")
            d12[t:t + len(site["mod"])] = site["mod"]
        write_overlay(12, bytes(d12))
        log.append("hp: 2 sites patched")

    rom.arm9OverlayTable = ndspy.code.saveOverlayTable(overlays)
    for line in log:
        print(f"      {line}")
    return rom


# --------------------------------------------------------------------- main

def build_korean_reference() -> tuple[Path, Path]:
    """Apply upstream Visual+ patch to Korean HG (if not already done)."""
    kor = find_rom(PROFILES["heartgold_kor"])
    out = WORKDIR / "hg_kor_visualplus.nds"
    if not out.exists():
        patch_dir = (Path.home() / "Desktop" / "HGSS ROMS" /
                     "포켓몬스터 비주얼+ 1.0.0 패치")
        patch = patch_dir / "하트골드_비주얼+_1.0.0.xdelta"
        WORKDIR.mkdir(parents=True, exist_ok=True)
        subprocess.run(["xdelta3", "-d", "-f", "-s", str(kor), str(patch),
                        str(out)], check=True)
    return kor, out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", nargs="+", default=list(GAMES),
                    choices=list(GAMES))
    ap.add_argument("--variants", nargs="+", default=list(VARIANTS),
                    choices=list(VARIANTS))
    args = ap.parse_args()

    kor_clean_path, kor_mod_path = build_korean_reference()
    print(f"KOR clean : {kor_clean_path.name}")
    print(f"KOR mod   : {kor_mod_path.name}")
    kor_clean = ndspy.rom.NintendoDSRom.fromFile(str(kor_clean_path))
    kor_mod = ndspy.rom.NintendoDSRom.fromFile(str(kor_mod_path))
    print("extracting components...")
    comp = extract_components(kor_clean, kor_mod)

    manifest = {"visual_plus_version": VISUAL_PLUS_VERSION, "builds": []}
    for game in args.games:
        usa_path = find_rom(PROFILES[GAMES[game]["profile"]])
        print(f"\n=== {game} ({usa_path.name}) ===")
        for variant in args.variants:
            print(f"  -> {variant}")
            rom = ndspy.rom.NintendoDSRom.fromFile(str(usa_path))
            rom = apply_variant(rom, comp, variant)
            out_rom = WORKDIR / "out" / f"{game}-english-visual-plus-{variant}.nds"
            out_rom.parent.mkdir(parents=True, exist_ok=True)
            rom.saveToFile(str(out_rom))

            patch_dir = RELEASE / game
            patch_dir.mkdir(parents=True, exist_ok=True)
            patch = patch_dir / (f"{game}-english-visual-plus-{variant}"
                                 f"-{VISUAL_PLUS_VERSION}.xdelta")
            subprocess.run(["xdelta3", "-e", "-f", "-9", "-s", str(usa_path),
                            str(out_rom), str(patch)], check=True)
            entry = {
                "game": game, "variant": variant,
                "patch": str(patch.relative_to(REPO_ROOT)),
                "patch_sha256": sha256(patch.read_bytes()),
                "source_rom_sha256": sha256(usa_path.read_bytes()),
                "patched_rom_sha256": sha256(out_rom.read_bytes()),
            }
            manifest["builds"].append(entry)
            print(f"      patch: {patch.name} "
                  f"({patch.stat().st_size} bytes)")

    (RELEASE / "release_manifest.json").write_text(
        json.dumps(manifest, indent=2))
    print(f"\nmanifest: release/release_manifest.json "
          f"({len(manifest['builds'])} builds)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
