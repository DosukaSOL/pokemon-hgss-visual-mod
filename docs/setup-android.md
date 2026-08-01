# Android Installation (UniPatcher)

Patch your ROM directly on an Android device with
[UniPatcher](https://play.google.com/store/apps/details?id=org.emunix.unipatcher)
(free, open source, supports xdelta).

## Steps

1. Install **UniPatcher** from the Play Store or F-Droid.
2. Copy to your device:
   - your **clean USA ROM** (`.nds`) — dumped from your own cartridge
   - the **`.xdelta` patch** for your game/variant from
     [Download](download.md)
3. Open UniPatcher → tap **☰ → Apply patch**.
4. **Patch file**: select the `.xdelta` file.
5. **ROM file**: select your clean `.nds`.
6. **Output file**: choose a name, e.g. `HeartGold-VisualPlus-Full.nds`.
7. Tap the ✔ / **Apply** button and wait for *"Patching complete"*.
8. Load the output `.nds` in your emulator of choice
   (melonDS, DraStic, melonDualDS, …).

## Notes

- xdelta patches are **checksummed**: if UniPatcher reports a source-file
  error, your ROM is not the expected clean dump — see
  [Troubleshooting](troubleshooting.md) and the
  [Compatibility Matrix](compatibility.md).
- Keep your clean ROM as a backup; patch onto a copy.
