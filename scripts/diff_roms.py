#!/usr/bin/env python3
"""Diff two NDS ROMs at the filesystem level.

Compares arm9, arm7, every overlay, banner, header, and every file in the
NitroFS, reporting what changed. Output: JSON report + human-readable summary.

Usage:
    python scripts/diff_roms.py CLEAN.nds MODDED.nds -o analysis/hg_kor_diff.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import ndspy.rom


def h(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def walk_files(rom: ndspy.rom.NintendoDSRom) -> dict[str, bytes]:
    """Map every NitroFS path -> file bytes."""
    out: dict[str, bytes] = {}
    for i, data in enumerate(rom.files):
        name = rom.filenames.filenameOf(i)
        out[name if name else f"<unnamed:{i}>"] = data
    return out


def diff_roms(clean_path: Path, mod_path: Path) -> dict:
    a = ndspy.rom.NintendoDSRom.fromFile(str(clean_path))
    b = ndspy.rom.NintendoDSRom.fromFile(str(mod_path))

    report: dict = {
        "clean": str(clean_path),
        "modded": str(mod_path),
        "code": {},
        "overlays": {"changed": [], "added": [], "removed": []},
        "files": {"changed": [], "added": [], "removed": []},
    }

    for name in ("arm9", "arm7", "arm9PostData", "iconBanner"):
        da, db = getattr(a, name), getattr(b, name)
        if bytes(da) != bytes(db):
            report["code"][name] = {
                "clean_sha256": h(bytes(da)), "modded_sha256": h(bytes(db)),
                "clean_size": len(da), "modded_size": len(db),
            }

    ov_a = {oid: bytes(a.files[o.fileID])
            for oid, o in a.loadArm9Overlays().items()}
    ov_b = {oid: bytes(b.files[o.fileID])
            for oid, o in b.loadArm9Overlays().items()}
    for oid in sorted(set(ov_a) | set(ov_b)):
        if oid not in ov_a:
            report["overlays"]["added"].append(oid)
        elif oid not in ov_b:
            report["overlays"]["removed"].append(oid)
        elif ov_a[oid] != ov_b[oid]:
            report["overlays"]["changed"].append({
                "id": oid,
                "clean_size": len(ov_a[oid]), "modded_size": len(ov_b[oid]),
                "clean_sha256": h(ov_a[oid]), "modded_sha256": h(ov_b[oid]),
            })

    fa, fb = walk_files(a), walk_files(b)
    overlay_ids = ({o.fileID for o in a.loadArm9Overlays().values()} |
                   {o.fileID for o in b.loadArm9Overlays().values()})
    overlay_names = {f"<unnamed:{i}>" for i in overlay_ids} | {
        n for i in overlay_ids
        if (n := a.filenames.filenameOf(i))}
    for name in sorted(set(fa) | set(fb)):
        if name in overlay_names:
            continue  # overlays reported separately
        if name not in fa:
            report["files"]["added"].append(
                {"path": name, "size": len(fb[name])})
        elif name not in fb:
            report["files"]["removed"].append(
                {"path": name, "size": len(fa[name])})
        elif fa[name] != fb[name]:
            report["files"]["changed"].append({
                "path": name,
                "clean_size": len(fa[name]), "modded_size": len(fb[name]),
                "clean_sha256": h(fa[name]), "modded_sha256": h(fb[name]),
            })
    return report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("clean", type=Path)
    ap.add_argument("modded", type=Path)
    ap.add_argument("-o", "--output", type=Path, required=True)
    args = ap.parse_args()

    report = diff_roms(args.clean, args.modded)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False))

    n_code = len(report["code"])
    n_ov = len(report["overlays"]["changed"])
    n_f = len(report["files"]["changed"])
    print(f"code sections changed : {n_code} "
          f"({', '.join(report['code']) or 'none'})")
    print(f"overlays changed      : {n_ov} "
          f"({', '.join(str(o['id']) for o in report['overlays']['changed'])})")
    print(f"files changed         : {n_f}")
    for fch in report["files"]["changed"]:
        print(f"  ~ {fch['path']} ({fch['clean_size']} -> {fch['modded_size']})")
    for fad in report["files"]["added"]:
        print(f"  + {fad['path']} ({fad['size']})")
    for frm in report["files"]["removed"]:
        print(f"  - {frm['path']}")
    print(f"report written        : {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
