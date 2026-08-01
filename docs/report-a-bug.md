# Report a Bug

Please open an issue on the
[GitHub issue tracker](https://github.com/DosukaSOL/pokemon-hgss-visual-mod/issues)
with the following information:

## Required info

- **Game**: HeartGold or SoulSilver
- **Variant**: visual-only / safe / full / conservative-camera
- **Patch version**: e.g. 1.0.0
- **Platform**: real hardware (which flashcart), melonDS, DraStic, AYN Thor…
- **Clean ROM SHA-256** (before patching) — `shasum -a 256 rom.nds`
- **Patched ROM SHA-256** — must match the value in the
  [test report](reports/HeartGold_Test_Report.md) for your variant
- **What happened** vs **what you expected**
- **Where in the game** (map/route, battle type) — screenshots help a lot

## Please do NOT

- attach or link ROMs, save files containing ROM data, or extracted assets
- report bugs for patches applied on top of *other* mods — only clean USA
  ROMs are supported

Camera glitches on specific maps in the `full` variant are a known upstream
limitation — reports are still welcome so we can build a map blacklist for a
future `conservative-camera` tuning pass.
