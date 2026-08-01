#!/usr/bin/env python3
"""Locate and verify NDS ROMs by SHA-256 and NDS header.

Searches ~/Desktop/HGSS ROMS/ and local_data/input/roms/ for .nds files,
parses the NDS header (title, game code, maker, CRC16) and checks the
SHA-256 against the manifest in tests/rom_manifest.json.

ROMs are NEVER copied, moved, or committed by this script.
"""
from __future__ import annotations

import hashlib
import json
import struct
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "tests" / "rom_manifest.json"

SEARCH_DIRS = [
    Path.home() / "Desktop" / "HGSS ROMS",
    REPO_ROOT / "local_data" / "input" / "roms",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_nds_header(path: Path) -> dict:
    with path.open("rb") as f:
        hdr = f.read(0x160)
    if len(hdr) < 0x160:
        raise ValueError("file too small to be an NDS ROM")
    title = hdr[0x00:0x0C].rstrip(b"\x00").decode("ascii", "replace")
    game_code = hdr[0x0C:0x10].decode("ascii", "replace")
    maker = hdr[0x10:0x12].decode("ascii", "replace")
    unit_code = hdr[0x12]
    device_capacity = hdr[0x14]
    header_crc = struct.unpack_from("<H", hdr, 0x15E)[0]
    return {
        "title": title,
        "game_code": game_code,
        "maker": maker,
        "unit_code": unit_code,
        "size_mbit": (1 << device_capacity) * 128 // 8,
        "header_crc16": f"0x{header_crc:04X}",
    }


def find_roms() -> list[Path]:
    roms: list[Path] = []
    for d in SEARCH_DIRS:
        if d.is_dir():
            roms.extend(sorted(d.rglob("*.nds")))
    return roms


def main() -> int:
    manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    known = {e["sha256"]: e for e in manifest.get("roms", [])}

    roms = find_roms()
    if not roms:
        print("ERROR: no .nds files found in:", *SEARCH_DIRS, sep="\n  ")
        return 1

    ok = True
    found_roles: dict[str, Path] = {}
    for rom in roms:
        try:
            hdr = parse_nds_header(rom)
        except ValueError as e:
            print(f"[SKIP] {rom.name}: {e}")
            continue
        digest = sha256(rom)
        entry = known.get(digest)
        status = "VERIFIED" if entry else "UNKNOWN"
        role = entry["role"] if entry else "-"
        if entry:
            found_roles[role] = rom
        print(f"[{status}] {rom.name}")
        print(f"         title={hdr['title']} code={hdr['game_code']} "
              f"maker={hdr['maker']} crc={hdr['header_crc16']}")
        print(f"         sha256={digest}  role={role}")

    required = {e["role"] for e in manifest.get("roms", []) if e.get("required")}
    missing = required - set(found_roles)
    if missing:
        print(f"\nERROR: missing required ROMs: {', '.join(sorted(missing))}")
        ok = False
    else:
        print("\nAll required ROMs verified.")

    if "--json" in sys.argv:
        print(json.dumps({r: str(p) for r, p in found_roles.items()}))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
