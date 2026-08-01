#!/usr/bin/env python3
"""Byte-level analysis of Visual+ code changes (decompressed arm9/overlays).

For each changed code component, decompress both versions and report
contiguous changed byte ranges with hex context. Also inspects changed
data files to determine whether they are NARC archives and, if so,
which subfiles changed.

Usage:
    python scripts/analyze_changes.py CLEAN.nds MODDED.nds -o analysis/out.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import ndspy.rom
import ndspy.codeCompression
import ndspy.narc


def decompressed_arm9(rom: ndspy.rom.NintendoDSRom) -> bytes:
    data = bytes(rom.arm9)
    try:
        return bytes(ndspy.codeCompression.decompress(data))
    except Exception:
        return data


def decompressed_overlay(rom: ndspy.rom.NintendoDSRom, oid: int) -> bytes:
    ov = rom.loadArm9Overlays()[oid]
    data = bytes(rom.files[ov.fileID])
    if ov.compressed:
        try:
            return bytes(ndspy.codeCompression.decompress(data))
        except Exception:
            pass
    return data


def changed_ranges(a: bytes, b: bytes, merge_gap: int = 8) -> list[dict]:
    """Contiguous [start, end) ranges where a and b differ (nearby merged)."""
    n = min(len(a), len(b))
    ranges: list[list[int]] = []
    i = 0
    while i < n:
        if a[i] != b[i]:
            start = i
            while i < n and a[i] != b[i]:
                i += 1
            if ranges and start - ranges[-1][1] <= merge_gap:
                ranges[-1][1] = i
            else:
                ranges.append([start, i])
        else:
            i += 1
    out = []
    for s, e in ranges:
        out.append({
            "offset": f"0x{s:X}", "length": e - s,
            "clean_hex": a[max(0, s - 8):e + 8].hex(),
            "modded_hex": b[max(0, s - 8):e + 8].hex(),
        })
    if len(a) != len(b):
        out.append({"offset": f"0x{n:X}", "length": abs(len(a) - len(b)),
                    "note": f"size {len(a)} -> {len(b)} (tail)"})
    return out


def narc_subfile_diff(a_data: bytes, b_data: bytes) -> dict | None:
    try:
        na = ndspy.narc.NARC(a_data)
        nb = ndspy.narc.NARC(b_data)
    except Exception:
        return None
    changed, added, removed = [], [], []
    n = max(len(na.files), len(nb.files))
    for i in range(n):
        fa = na.files[i] if i < len(na.files) else None
        fb = nb.files[i] if i < len(nb.files) else None
        if fa is None:
            added.append({"index": i, "size": len(fb)})
        elif fb is None:
            removed.append({"index": i, "size": len(fa)})
        elif bytes(fa) != bytes(fb):
            changed.append({"index": i,
                            "clean_size": len(fa), "modded_size": len(fb)})
    return {"type": "NARC",
            "clean_count": len(na.files), "modded_count": len(nb.files),
            "changed": changed, "added": added, "removed": removed}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("clean", type=Path)
    ap.add_argument("modded", type=Path)
    ap.add_argument("-o", "--output", type=Path, required=True)
    args = ap.parse_args()

    a = ndspy.rom.NintendoDSRom.fromFile(str(args.clean))
    b = ndspy.rom.NintendoDSRom.fromFile(str(args.modded))
    report: dict = {"arm9": None, "overlays": {}, "data_files": {}}

    da, db = decompressed_arm9(a), decompressed_arm9(b)
    if da != db:
        r = changed_ranges(da, db)
        report["arm9"] = {"decompressed_sizes": [len(da), len(db)], "ranges": r}
        print(f"arm9 (decompressed {len(da)} vs {len(db)}): "
              f"{len(r)} changed range(s)")
        for c in r:
            print(f"  @{c['offset']} len={c['length']}")

    ov_ids_a = set(a.loadArm9Overlays())
    ov_ids_b = set(b.loadArm9Overlays())
    for oid in sorted(ov_ids_a & ov_ids_b):
        oa, ob = decompressed_overlay(a, oid), decompressed_overlay(b, oid)
        if oa != ob:
            r = changed_ranges(oa, ob)
            report["overlays"][oid] = {
                "decompressed_sizes": [len(oa), len(ob)], "ranges": r}
            print(f"overlay {oid} (decompressed {len(oa)} vs {len(ob)}): "
                  f"{len(r)} changed range(s)")
            for c in r:
                print(f"  @{c['offset']} len={c['length']}")

    for i, fdata in enumerate(a.files):
        if i >= len(b.files):
            break
        fb = b.files[i]
        if bytes(fdata) == bytes(fb):
            continue
        name = a.filenames.filenameOf(i) or f"<unnamed:{i}>"
        if name.startswith("<unnamed:"):
            continue  # overlays handled above
        nd = narc_subfile_diff(bytes(fdata), bytes(fb))
        report["data_files"][name] = nd or {"type": "raw",
                                            "clean_size": len(fdata),
                                            "modded_size": len(fb)}
        if nd:
            print(f"{name}: NARC {nd['clean_count']}->{nd['modded_count']} files; "
                  f"changed={[c['index'] for c in nd['changed']]} "
                  f"added={[x['index'] for x in nd['added']]} "
                  f"removed={[x['index'] for x in nd['removed']]}")
        else:
            print(f"{name}: raw binary changed "
                  f"({len(fdata)} -> {len(fb)})")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"report written: {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
