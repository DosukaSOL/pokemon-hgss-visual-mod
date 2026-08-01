# SoulSilver — English Visual+ Port Test Report

- Visual+ version: 1.0.0
- Date: 2026-08-01
- Result: **ALL TESTS PASSED** (68 automated checks)

All checks below were executed against this game's own ROMs and
builds — no results were reused from the other game.

## Release patches

| Variant | Patch | Patch SHA-256 | Patched ROM SHA-256 |
|---|---|---|---|
| visual-only | `soulsilver-english-visual-plus-visual-only-1.0.0.xdelta` | `5c0d269c3dac521c…` | `01a6ce42f035180a…` |
| safe | `soulsilver-english-visual-plus-safe-1.0.0.xdelta` | `d0882d334690a97d…` | `403e04a10a2e60f4…` |
| full | `soulsilver-english-visual-plus-full-1.0.0.xdelta` | `3c3827d031f4d706…` | `94c9162242aaf809…` |
| conservative-camera | `soulsilver-english-visual-plus-conservative-camera-1.0.0.xdelta` | `51dc4473e40789b8…` | `9b93cf2d85b5d565…` |

Source ROM (clean, user-supplied): SHA-256 `51d0f94a16af7d77c067b4cb7d821ba890a13203a2e2c76049623332c0582e20`

## Automated checks

| Variant | Check | Status | Detail |
|---|---|---|---|
| visual-only | patch round-trip | ✅ PASS | sha256 01a6ce42f035… |
| visual-only | game code unchanged | ✅ PASS | IPGE |
| visual-only | title unchanged | ✅ PASS |  |
| visual-only | banner unchanged | ✅ PASS |  |
| visual-only | map-header battle-bg ids (73) | ✅ PASS |  |
| visual-only | arm9 code cave + literal | ✅ PASS |  |
| visual-only | arm9 hook | ✅ PASS |  |
| visual-only | arm9 stored uncompressed | ✅ PASS |  |
| visual-only | ov123 runtime-patch target | ✅ PASS |  |
| visual-only | ov1 visual byte | ✅ PASS |  |
| visual-only | ov1 camera words (blend=0.0) | ✅ PASS |  |
| visual-only | ov12 HP site 1 (clean) | ✅ PASS |  |
| visual-only | ov12 HP site 2 (clean) | ✅ PASS |  |
| visual-only | a/0/0/7 subfiles | ✅ PASS | 72 replaced, rest untouched |
| visual-only | a/0/0/8 subfiles | ✅ PASS | 45 replaced, rest untouched |
| visual-only | a/2/6/2 subfiles | ✅ PASS | 2 replaced, rest untouched |
| visual-only | isolation sweep (all other files) | ✅ PASS | 513/513 identical |
| safe | patch round-trip | ✅ PASS | sha256 403e04a10a2e… |
| safe | game code unchanged | ✅ PASS | IPGE |
| safe | title unchanged | ✅ PASS |  |
| safe | banner unchanged | ✅ PASS |  |
| safe | map-header battle-bg ids (73) | ✅ PASS |  |
| safe | arm9 code cave + literal | ✅ PASS |  |
| safe | arm9 hook | ✅ PASS |  |
| safe | arm9 stored uncompressed | ✅ PASS |  |
| safe | ov123 runtime-patch target | ✅ PASS |  |
| safe | ov1 visual byte | ✅ PASS |  |
| safe | ov1 camera words (blend=0.0) | ✅ PASS |  |
| safe | ov12 HP site 1 (modded) | ✅ PASS |  |
| safe | ov12 HP site 2 (modded) | ✅ PASS |  |
| safe | a/0/0/7 subfiles | ✅ PASS | 72 replaced, rest untouched |
| safe | a/0/0/8 subfiles | ✅ PASS | 45 replaced, rest untouched |
| safe | a/2/6/2 subfiles | ✅ PASS | 2 replaced, rest untouched |
| safe | isolation sweep (all other files) | ✅ PASS | 513/513 identical |
| full | patch round-trip | ✅ PASS | sha256 94c9162242aa… |
| full | game code unchanged | ✅ PASS | IPGE |
| full | title unchanged | ✅ PASS |  |
| full | banner unchanged | ✅ PASS |  |
| full | map-header battle-bg ids (73) | ✅ PASS |  |
| full | arm9 code cave + literal | ✅ PASS |  |
| full | arm9 hook | ✅ PASS |  |
| full | arm9 stored uncompressed | ✅ PASS |  |
| full | ov123 runtime-patch target | ✅ PASS |  |
| full | ov1 visual byte | ✅ PASS |  |
| full | ov1 camera words (blend=1.0) | ✅ PASS |  |
| full | ov12 HP site 1 (modded) | ✅ PASS |  |
| full | ov12 HP site 2 (modded) | ✅ PASS |  |
| full | a/0/0/7 subfiles | ✅ PASS | 72 replaced, rest untouched |
| full | a/0/0/8 subfiles | ✅ PASS | 45 replaced, rest untouched |
| full | a/2/6/2 subfiles | ✅ PASS | 2 replaced, rest untouched |
| full | isolation sweep (all other files) | ✅ PASS | 513/513 identical |
| conservative-camera | patch round-trip | ✅ PASS | sha256 9b93cf2d85b5… |
| conservative-camera | game code unchanged | ✅ PASS | IPGE |
| conservative-camera | title unchanged | ✅ PASS |  |
| conservative-camera | banner unchanged | ✅ PASS |  |
| conservative-camera | map-header battle-bg ids (73) | ✅ PASS |  |
| conservative-camera | arm9 code cave + literal | ✅ PASS |  |
| conservative-camera | arm9 hook | ✅ PASS |  |
| conservative-camera | arm9 stored uncompressed | ✅ PASS |  |
| conservative-camera | ov123 runtime-patch target | ✅ PASS |  |
| conservative-camera | ov1 visual byte | ✅ PASS |  |
| conservative-camera | ov1 camera words (blend=0.5) | ✅ PASS |  |
| conservative-camera | ov12 HP site 1 (modded) | ✅ PASS |  |
| conservative-camera | ov12 HP site 2 (modded) | ✅ PASS |  |
| conservative-camera | a/0/0/7 subfiles | ✅ PASS | 72 replaced, rest untouched |
| conservative-camera | a/0/0/8 subfiles | ✅ PASS | 45 replaced, rest untouched |
| conservative-camera | a/2/6/2 subfiles | ✅ PASS | 2 replaced, rest untouched |
| conservative-camera | isolation sweep (all other files) | ✅ PASS | 513/513 identical |

## Manual acceptance criteria (to be confirmed on hardware/emulator)

- [ ] Game boots to title screen and starts a new game
- [ ] Wild battle shows new Visual+ battle background
- [ ] Trainer battle shows new Visual+ battle background
- [ ] HP bar drains at increased speed (Full/Safe/Conservative)
- [ ] 3D camera active in overworld (Full/Conservative only)
- [ ] Known camera-glitch maps checked (Full variant)
- [ ] Save/load works; existing saves compatible
- [ ] No graphical corruption in battle intro sequences
