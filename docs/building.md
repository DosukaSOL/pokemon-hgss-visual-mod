# Building From Source

Rebuild all patches yourself from your own legally dumped ROMs.

## Prerequisites

- Python 3.9+
- `xdelta3` (`brew install xdelta` / `apt install xdelta3`)
- Your own legally dumped ROMs:
  - Pokémon HeartGold (Korea) — Visual+ upstream base
  - Pokémon HeartGold (USA) and/or SoulSilver (USA) — port targets
- The upstream **Visual+ 1.0.0** patch files (from the original Korean
  release by MinT ChoK)

Place ROMs in `~/Desktop/HGSS ROMS/` (any layout — they're found by
SHA-256) or under `local_data/input/roms/`. Nothing under `local_data/` is
ever committed.

## Setup

```bash
git clone https://github.com/DosukaSOL/pokemon-hgss-visual-mod
cd pokemon-hgss-visual-mod
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Pipeline

```bash
# 1. locate + verify all ROMs (SHA-256 + NDS header)
.venv/bin/python scripts/verify_roms.py

# 2. build: extracts Visual+ components from the Korean pair and applies
#    them to the USA ROMs with per-site verification; emits release/*.xdelta
.venv/bin/python scripts/port.py

# 3. validate: patch round-trips, component presence, isolation sweeps;
#    writes docs/reports/*_Test_Report.md
.venv/bin/python scripts/validate.py
```

Restrict to one game or variant:

```bash
.venv/bin/python scripts/port.py --games heartgold --variants full safe
```

## Analysis tools

```bash
# filesystem-level ROM diff (arm9/overlays/every file)
.venv/bin/python scripts/diff_roms.py CLEAN.nds MODDED.nds -o out.json

# byte-level analysis (decompressed code, NARC subfile diffs)
.venv/bin/python scripts/analyze_changes.py CLEAN.nds MODDED.nds -o out.json
```

## How the port works

The Korean Visual+ mod decomposes into three independent components:

| Component | Where | Port strategy |
|---|---|---|
| Battle backgrounds | NARCs `a/0/0/7`, `a/0/0/8`, `a/2/6/2` + 73 map-header bytes in arm9 + a small arm9 code cave | subfiles byte-identical across regions → drop-in; map table located at −1708 bytes in USA (verified per-entry); cave RAM literal retargeted to the USA overlay-123 address |
| HP drain speed | overlay 12, two constant sites | located by unique byte-pattern match, never by offset |
| 3D camera | overlay 1, 81-word parameter table | clean table byte-identical across regions → drop-in; `conservative-camera` blends each word 50 % |

Every edit verifies the expected clean bytes first and the build **fails
hard** on any mismatch — HeartGold and SoulSilver are verified independently.

## Adding a new game (e.g. Platinum)

1. Add its profile + manifest entry in [scripts/profiles.py](../scripts/profiles.py)
   and `tests/rom_manifest.json`.
2. Run the analysis scripts against the upstream Korean patch for that game.
3. Extend `GAMES` in [scripts/port.py](../scripts/port.py) — then re-verify
   every component offset independently. **Never assume offsets carry over.**
