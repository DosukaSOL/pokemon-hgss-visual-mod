# Pokémon HG/SS Visual Mod — Visual+ English Port

English (USA) port of **Pokémon Visual+ v1.0.0**, a Korean visual enhancement
mod for Pokémon HeartGold, created by **민트초크 (MinT ChoK)** with battle
background artwork by **Young** (Pokémon Another Red). This project ports the
mod to the English HeartGold *and* SoulSilver ROMs and distributes it as
xdelta patches only.

## What Visual+ changes

1. **New battle backgrounds** — redrawn, more vivid battle background images
2. **Enhanced 3D camera** — a more dramatic overworld camera angle
3. **Faster HP bar** — HP drains ~7–8× faster in battle

## Variants

| Variant | Backgrounds | Fast HP | 3D Camera |
|---|---|---|---|
| `visual-only` | ✅ | ❌ | ❌ |
| `safe` | ✅ | ✅ | ❌ |
| `full` | ✅ | ✅ | ✅ full |
| `conservative-camera` | ✅ | ✅ | ✅ 50 % blend |

The upstream mod notes the full 3D camera can glitch on a few maps — pick
`safe` or `conservative-camera` if that bothers you.

## Supported games

| Game | Status |
|---|---|
| Pokémon HeartGold (USA) | ✅ released |
| Pokémon SoulSilver (USA) | ✅ released |
| Pokémon Platinum (USA) | 🔜 planned |
| Pokémon Diamond / Pearl | 🔮 future |
| Pokémon Black / White | 🔮 future |

## Quick start

1. Obtain a **legal dump of your own cartridge** (see [Legal](docs/legal.md)).
2. Download the patch for your game/variant from the
   [Releases page](../../releases) or see [docs/download.md](docs/download.md).
3. Apply with xdelta ([Windows](docs/setup-windows.md) ·
   [Android/UniPatcher](docs/setup-android.md) ·
   [macOS/Linux](docs/setup-macos-linux.md) ·
   [AYN Thor](docs/setup-ayn-thor.md)).
4. Play on real hardware or an emulator
   ([melonDualDS guide](docs/setup-melondualds.md)).

Expected clean ROM checksums are listed in
[docs/compatibility.md](docs/compatibility.md).

## Building from source

See [docs/building.md](docs/building.md). Short version:

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
brew install xdelta                      # or your package manager
.venv/bin/python scripts/verify_roms.py  # locate + verify your ROMs
.venv/bin/python scripts/port.py         # build all 8 patches
.venv/bin/python scripts/validate.py     # run the full test suite
```

Test reports: [HeartGold](docs/reports/HeartGold_Test_Report.md) ·
[SoulSilver](docs/reports/SoulSilver_Test_Report.md)

## Legal

**This project does not distribute ROMs.** Users must supply a legally
obtained ROM dump from a game they own where permitted by applicable law.
The repository contains only tools, documentation, and binary *difference*
patches. See [docs/legal.md](docs/legal.md).

## Credits

- **민트초크 (MinT ChoK)** — original Visual+ mod
- **Young** — battle background artwork (Pokémon Another Red)
- **KaioShin / Josh MacDonald** — xdeltaUI / xdelta
- **RoadrunnerWMC** — ndspy
- English port tooling — this repository

See [docs/credits.md](docs/credits.md).
