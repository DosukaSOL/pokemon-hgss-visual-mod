# Windows Setup

Two options: the graphical **xdeltaUI** or the **xdelta3** command line.

## Option A — xdeltaUI (graphical)

1. Download xdeltaUI (bundled in many romhacking tool packs, or from
   romhacking.net).
2. Run `xdeltaUI.exe`.
3. **Patch**: click *Open…* and select your `.xdelta` file from
   [Download](download.md).
4. **Source File**: click *Open…* and select your **clean USA ROM** (`.nds`).
5. **Output File**: click *…* and choose where to save the patched ROM.
6. Click **Patch**. Wait for *"File Patched Successfully"*.

## Option B — xdelta3 (command line)

1. Download `xdelta3.exe` from the
   [xdelta releases](https://github.com/jmacd/xdelta/releases) or install
   via `winget install xdelta` / `choco install xdelta3` where available.
2. In PowerShell:

```powershell
xdelta3 -d -s "Pokemon - HeartGold Version (USA).nds" `
  heartgold-english-visual-plus-full-1.0.0.xdelta `
  HeartGold-VisualPlus-Full.nds
```

## Verify (optional but recommended)

```powershell
Get-FileHash HeartGold-VisualPlus-Full.nds -Algorithm SHA256
```

Compare against the patched-ROM checksum in the
[test report](reports/HeartGold_Test_Report.md) for your variant.
