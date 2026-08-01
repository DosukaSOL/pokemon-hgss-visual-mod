# Changelog

## 1.0.0 — 2026-08-01

First release of the English port, based on **Visual+ v1.0.0** (Korean
HeartGold, by MinT ChoK).

### Added
- **HeartGold (USA)**: `visual-only`, `safe`, `full`, `conservative-camera`
  patches
- **SoulSilver (USA)**: `visual-only`, `safe`, `full`, `conservative-camera`
  patches — independently analyzed and verified (upstream has no SoulSilver
  version)
- New `conservative-camera` variant (50 % camera strength), not present
  upstream
- **"English Patch By Dosuka"** credit line on the boot copyright screen,
  beneath the original mod credits (all variants, both games)
- Automated build + validation pipeline (`scripts/`), per-game test reports
  and compatibility matrices

### Notes
- The Korean mod's banner/title text change is intentionally **not** ported
  (English banner kept)
- The upstream "no 3D camera" patch corresponds to our `safe` variant
