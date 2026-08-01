# Troubleshooting

## "xdelta3: source file mismatch" / UniPatcher checksum error

Your ROM is not the expected clean USA dump. xdelta patches verify the
source before patching — this protects you from corrupting the wrong file.

- Verify your ROM's SHA-256 against the
  [Compatibility Matrix](compatibility.md).
- Common causes: trimmed ROMs, EU/JP/KO region dumps, ROMs already patched
  with another mod, bad dumps.
- Fix: re-dump your cartridge or locate your original untrimmed dump.

## Game boots but looks vanilla (no new backgrounds)

You loaded the **unpatched** ROM. Load the output file you created during
patching.

## Camera looks wrong / glitches on some maps

The upstream mod documents that the **full 3D camera glitches on a few
maps**. Options:

- use the `conservative-camera` variant (50 % camera strength), or
- use the `safe` variant (no camera changes at all).

## Crash or freeze at battle start

- Confirm you patched a **clean** ROM (see checksum note above).
- Verify the patched ROM's SHA-256 matches the value in the
  [test report](reports/HeartGold_Test_Report.md) for your game/variant.
- In melonDS, use the OpenGL renderer and disable cheats.

## Anti-piracy / white screens on flashcart

- Update your flashcart kernel/firmware.
- Some old flashcarts mishandle ROMs whose arm9 is stored uncompressed
  (this port stores it uncompressed, like the original Korean mod). Use a
  current kernel or an emulator.

## Save issues

Visual+ does not touch the save system. Saves from a clean English ROM are
compatible with the patched ROM and vice versa (same game code, same save
type).

Still stuck? [Report a bug](report-a-bug.md).
