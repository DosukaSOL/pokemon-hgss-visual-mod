# Legal

**This project does not distribute ROMs.** Users must supply a legally
obtained ROM dump from a game they own where permitted by applicable law.

## What this repository contains

- Source code of the porting/verification tooling (original work)
- Documentation
- Binary **difference patches** (`.xdelta`) that transform a user-supplied
  clean ROM into the modified version. Patches contain only the differences
  introduced by the mod.

## What this repository will never contain

- Nintendo ROMs, in whole or in part
- Extracted game assets, archives, executables or other copyrighted
  Nintendo content
- BIOS or firmware images

The `.gitignore` enforces this: `local_data/`, `*.nds`, extracted archives
and built ROMs are excluded from version control.

## Trademarks & copyright

Pokémon, Nintendo DS, and all related names are trademarks of
Nintendo / Creatures Inc. / GAME FREAK inc. This is an unofficial fan
project, not affiliated with or endorsed by Nintendo.

## Upstream mod

Visual+ was created by **민트초크 (MinT ChoK)**; battle background artwork by
**Young** (used in the original mod with the artist's permission). This
English port redistributes their work in patch form with attribution.
Records of redistribution permissions are kept in
`local_data/input/permissions/` (not published). If you are a rights holder
of the upstream mod and want changes to this distribution,
please [open an issue](report-a-bug.md).

## Your responsibility

Laws on private copying and format-shifting differ by country. Only dump
and patch games you own, where your local law permits it.
