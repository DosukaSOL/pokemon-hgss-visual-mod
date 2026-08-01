# macOS / Linux Setup

## 1. Install xdelta3

```bash
# macOS
brew install xdelta

# Debian/Ubuntu
sudo apt install xdelta3

# Fedora
sudo dnf install xdelta

# Arch
sudo pacman -S xdelta3
```

## 2. Apply the patch

```bash
xdelta3 -d -s "Pokemon - HeartGold Version (USA).nds" \
  heartgold-english-visual-plus-full-1.0.0.xdelta \
  HeartGold-VisualPlus-Full.nds
```

Replace the file names for SoulSilver / other variants accordingly.

## 3. Verify

```bash
shasum -a 256 HeartGold-VisualPlus-Full.nds     # macOS
sha256sum HeartGold-VisualPlus-Full.nds         # Linux
```

Compare with the patched-ROM checksums in the
[HeartGold](reports/HeartGold_Test_Report.md) /
[SoulSilver](reports/SoulSilver_Test_Report.md) test reports.

## 4. Play

Load the patched `.nds` in melonDS, DeSmuME, or copy it to your flashcart.
