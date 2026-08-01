# AYN Thor Setup

The AYN Thor runs Android, so patching works exactly like any Android device
— then you play in your preferred DS emulator.

## 1. Patch the ROM

Follow the [Android Installation guide](setup-android.md) (UniPatcher) on the
Thor itself, or patch on a PC ([Windows](setup-windows.md) /
[macOS/Linux](setup-macos-linux.md)) and copy the patched `.nds` over via
USB / SD card.

## 2. Emulator setup

Recommended on the Thor:

- **melonDS (Android)** — accurate, active development
- **melonDualDS** — dual-screen layouts tuned for the Thor's screen; see the
  [melonDualDS guide](setup-melondualds.md)
- **DraStic** — fastest, but less accurate 3D; the Visual+ camera and battle
  backgrounds render fine in our testing notes, but melonDS is preferred

Suggested settings:

| Setting | Value |
|---|---|
| Renderer | OpenGL |
| Internal resolution | 2× or 3× (Thor handles it) |
| Screen layout | vertical (main screen large) |
| Frameskip | off |

## 3. Verify

Start a wild battle — you should immediately see the new Visual+ battle
background. If the game boots but backgrounds look vanilla, you loaded the
wrong (unpatched) ROM file.
