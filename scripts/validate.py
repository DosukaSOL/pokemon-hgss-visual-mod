#!/usr/bin/env python3
"""Automated validation of the English Visual+ builds.

For each game (independently — no results are shared between HG and SS):
  1. Patch round-trip: apply each release .xdelta to the verified clean USA
     ROM with xdelta3 and confirm the output SHA-256 matches the manifest.
  2. Header integrity: game code, title and banner unchanged.
  3. Component presence: every intended byte edit is present in the built
     ROM (map-header ids, code cave, hook, null pointer, overlay 1 camera
     words / visual byte, overlay 12 HP constants, NARC subfiles).
  4. Isolation: every file NOT intended to change is byte-identical to the
     clean ROM (full NitroFS sweep).

Writes docs/reports/HeartGold_Test_Report.md and SoulSilver_Test_Report.md.

Usage:
    python scripts/validate.py [--games heartgold soulsilver]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

import ndspy.narc
import ndspy.rom

sys.path.insert(0, str(Path(__file__).resolve().parent))
from profiles import PROFILES, find_rom  # noqa: E402
import port  # noqa: E402
from port import (  # noqa: E402
    CAVE_LITERAL_USA, CAVE_OFFSET, GAMES, HOOK_MOD, HOOK_OFFSET, HP_SITES,
    MAP_TABLE_DELTA_KOR_TO_USA, NULLPTR_OFFSET, OV123_SIG, RELEASE, VARIANTS,
    VISUAL_PLUS_VERSION, WORKDIR, arm9_decompressed, overlay_decompressed,
    sha256,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = REPO_ROOT / "docs" / "reports"
GAME_TITLES = {"heartgold": "HeartGold", "soulsilver": "SoulSilver"}


class Result:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str, str]] = []  # variant, test, status, detail
        self.failed = 0

    def add(self, variant: str, test: str, ok: bool, detail: str = "") -> None:
        self.rows.append((variant, test, "PASS" if ok else "FAIL", detail))
        if not ok:
            self.failed += 1
        mark = "ok" if ok else "FAIL"
        print(f"    [{mark:4s}] {variant:20s} {test} {detail}")


def validate_game(game: str, comp: dict, manifest: dict) -> Result:
    res = Result()
    clean_path = find_rom(PROFILES[GAMES[game]["profile"]])
    clean = ndspy.rom.NintendoDSRom.fromFile(str(clean_path))
    clean_files = {i: bytes(d) for i, d in enumerate(clean.files)}
    builds = [b for b in manifest["builds"] if b["game"] == game]

    for b in builds:
        variant = b["variant"]
        opts = VARIANTS[variant]
        built_path = (WORKDIR / "out" /
                      f"{game}-english-visual-plus-{variant}.nds")

        # 1. patch round-trip
        with tempfile.NamedTemporaryFile(suffix=".nds") as tmp:
            proc = subprocess.run(
                ["xdelta3", "-d", "-f", "-s", str(clean_path),
                 str(REPO_ROOT / b["patch"]), tmp.name],
                capture_output=True)
            rt_ok = proc.returncode == 0
            digest = sha256(Path(tmp.name).read_bytes()) if rt_ok else "-"
            res.add(variant, "patch round-trip",
                    rt_ok and digest == b["patched_rom_sha256"],
                    f"sha256 {digest[:12]}…")

        rom = ndspy.rom.NintendoDSRom.fromFile(str(built_path))

        # 2. header + banner integrity
        res.add(variant, "game code unchanged",
                rom.idCode == clean.idCode, rom.idCode.decode())
        res.add(variant, "title unchanged", rom.name == clean.name)
        res.add(variant, "banner unchanged",
                bytes(rom.iconBanner) == bytes(clean.iconBanner))

        # 3. component presence
        a9 = arm9_decompressed(rom)
        map_ok = all(
            a9[e["kor_off"] + MAP_TABLE_DELTA_KOR_TO_USA] == e["mod"]
            for e in comp["map_edits"])
        res.add(variant, "map-header battle-bg ids (73)", map_ok)

        cave = bytearray(comp["cave_kor"])
        idx = cave.index(port.CAVE_LITERAL_KOR.to_bytes(4, "little"))
        cave[idx:idx + 4] = CAVE_LITERAL_USA.to_bytes(4, "little")
        res.add(variant, "arm9 code cave + literal",
                a9[CAVE_OFFSET:CAVE_OFFSET + len(cave)] == bytes(cave))
        res.add(variant, "arm9 hook",
                a9[HOOK_OFFSET:HOOK_OFFSET + 4] == HOOK_MOD)
        res.add(variant, "arm9 stored uncompressed",
                a9[NULLPTR_OFFSET:NULLPTR_OFFSET + 4] == b"\x00" * 4
                and len(bytes(rom.arm9)) == len(a9))
        ov123 = overlay_decompressed(rom, 123)
        base = CAVE_LITERAL_USA - rom.loadArm9Overlays()[123].ramAddress
        res.add(variant, "ov123 runtime-patch target",
                int.from_bytes(ov123[base:base + 4], "little") == OV123_SIG)

        d1 = overlay_decompressed(rom, 1)
        e = comp["ov1_visual"]
        res.add(variant, "ov1 visual byte", d1[e["off"]] == e["mod"])
        blend = {"full": 1.0, "conservative": 0.5, None: 0.0}[opts["camera"]]
        cam_ok = all(
            int.from_bytes(d1[w["off"]:w["off"] + 4], "little", signed=True)
            == round(w["clean"] + (w["mod"] - w["clean"]) * blend)
            for w in comp["camera_words"])
        res.add(variant, f"ov1 camera words (blend={blend})", cam_ok)

        d12 = overlay_decompressed(rom, 12)
        for i, site in enumerate(HP_SITES):
            want = site["mod"] if opts["hp"] else site["clean"]
            t = site["target_at"]
            expect = bytearray(site["pattern"])
            expect[t:t + len(want)] = want  # pattern may overlap the target
            pos = d12.find(bytes(expect))
            res.add(variant, f"ov12 HP site {i + 1} "
                    f"({'modded' if opts['hp'] else 'clean'})",
                    pos != -1 and
                    d12[pos + t:pos + t + len(want)] == want)

        for path, edits in comp["narc_edits"].items():
            fid = rom.filenames.idOf(path)
            narc = ndspy.narc.NARC(bytes(rom.files[fid]))
            narc_clean = ndspy.narc.NARC(clean_files[fid])
            ok_changed = all(bytes(narc.files[i]) == e["data"]
                             for i, e in edits.items())
            ok_rest = all(bytes(narc.files[i]) == bytes(narc_clean.files[i])
                          for i in range(len(narc.files)) if i not in edits)
            res.add(variant, f"{path} subfiles",
                    ok_changed and ok_rest,
                    f"{len(edits)} replaced, rest untouched")

        # 4. isolation sweep: everything else identical to clean
        overlays = rom.loadArm9Overlays()
        touched_fids = {overlays[oid].fileID for oid in (1, 12)}
        touched_fids |= {rom.filenames.idOf(p) for p in comp["narc_edits"]}
        diffs = [i for i, d in enumerate(rom.files)
                 if i not in touched_fids and bytes(d) != clean_files[i]]
        res.add(variant, "isolation sweep (all other files)",
                not diffs, f"{len(rom.files) - len(diffs)}/{len(rom.files)} "
                f"identical" + (f"; unexpected: {diffs[:5]}" if diffs else ""))
    return res


def write_report(game: str, res: Result, manifest: dict) -> Path:
    title = GAME_TITLES[game]
    builds = [b for b in manifest["builds"] if b["game"] == game]
    lines = [
        f"# {title} — English Visual+ Port Test Report",
        "",
        f"- Visual+ version: {VISUAL_PLUS_VERSION}",
        f"- Date: {date.today().isoformat()}",
        f"- Result: **{'ALL TESTS PASSED' if res.failed == 0 else f'{res.failed} FAILURES'}**"
        f" ({len(res.rows)} automated checks)",
        "",
        "All checks below were executed against this game's own ROMs and",
        "builds — no results were reused from the other game.",
        "",
        "## Release patches",
        "",
        "| Variant | Patch | Patch SHA-256 | Patched ROM SHA-256 |",
        "|---|---|---|---|",
    ]
    for b in builds:
        lines.append(f"| {b['variant']} | `{Path(b['patch']).name}` | "
                     f"`{b['patch_sha256'][:16]}…` | "
                     f"`{b['patched_rom_sha256'][:16]}…` |")
    lines += [
        "",
        f"Source ROM (clean, user-supplied): SHA-256 "
        f"`{builds[0]['source_rom_sha256']}`",
        "",
        "## Automated checks",
        "",
        "| Variant | Check | Status | Detail |",
        "|---|---|---|---|",
    ]
    for variant, test, status, detail in res.rows:
        mark = "✅" if status == "PASS" else "❌"
        lines.append(f"| {variant} | {test} | {mark} {status} | {detail} |")
    lines += [
        "",
        "## Manual acceptance criteria (to be confirmed on hardware/emulator)",
        "",
        "- [ ] Game boots to title screen and starts a new game",
        "- [ ] Wild battle shows new Visual+ battle background",
        "- [ ] Trainer battle shows new Visual+ battle background",
        "- [ ] HP bar drains at increased speed (Full/Safe/Conservative)",
        "- [ ] 3D camera active in overworld (Full/Conservative only)",
        "- [ ] Known camera-glitch maps checked (Full variant)",
        "- [ ] Save/load works; existing saves compatible",
        "- [ ] No graphical corruption in battle intro sequences",
        "",
    ]
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    out = REPORT_DIR / f"{title}_Test_Report.md"
    out.write_text("\n".join(lines))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", nargs="+", default=list(GAMES),
                    choices=list(GAMES))
    args = ap.parse_args()

    manifest = json.loads((RELEASE / "release_manifest.json").read_text())
    kor_clean_path, kor_mod_path = port.build_korean_reference()
    kor_clean = ndspy.rom.NintendoDSRom.fromFile(str(kor_clean_path))
    kor_mod = ndspy.rom.NintendoDSRom.fromFile(str(kor_mod_path))
    comp = port.extract_components(kor_clean, kor_mod)

    failed = 0
    for game in args.games:
        print(f"\n=== validating {game} ===")
        res = validate_game(game, comp, manifest)
        report = write_report(game, res, manifest)
        print(f"  report: {report.relative_to(REPO_ROOT)}")
        failed += res.failed
    print(f"\n{'ALL TESTS PASSED' if failed == 0 else f'{failed} FAILURES'}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
