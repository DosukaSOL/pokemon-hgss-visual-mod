# melonDualDS Setup

[melonDualDS](https://github.com/melonDS-emu) -style dual-screen setups work
great with Visual+ since the mod's battle backgrounds and 3D camera benefit
from a large, high-resolution main screen.

## Steps

1. Install melonDualDS (or melonDS with dual-window layout) for your
   platform.
2. Patch your ROM first — see [Windows](setup-windows.md),
   [Android](setup-android.md) or [macOS/Linux](setup-macos-linux.md).
3. `File → Open ROM` and select the **patched** `.nds`.
4. Recommended settings:

| Setting | Value |
|---|---|
| Renderer | OpenGL |
| Internal resolution | 2×–4× |
| Screen layout | dual window / one screen per display |
| VSync | on |
| JIT | on (desktop) |

5. Firmware/BIOS: melonDS requires DS BIOS/firmware dumps from **your own
   console** — same legal rules as ROMs, see [Legal](legal.md).

## Known good

Both HeartGold and SoulSilver English Visual+ builds boot and run in
melonDS-core-based emulators; see the per-game
[compatibility matrices](compatibility.md).
