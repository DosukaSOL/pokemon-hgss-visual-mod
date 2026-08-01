# HeartGold — English Visual+ Port Test Report

- Visual+ version: 1.0.0
- Date: 2026-08-01
- Result: **ALL TESTS PASSED** (68 automated checks)

All checks below were executed against this game's own ROMs and
builds — no results were reused from the other game.

## Release patches

| Variant | Patch | Patch SHA-256 | Patched ROM SHA-256 |
|---|---|---|---|
| visual-only | `heartgold-english-visual-plus-visual-only-1.0.0.xdelta` | `e3f28caffe3af2b4…` | `ad2afac2eea92516…` |
| safe | `heartgold-english-visual-plus-safe-1.0.0.xdelta` | `c781dbea899cffa2…` | `4d9219bee5bf0653…` |
| full | `heartgold-english-visual-plus-full-1.0.0.xdelta` | `78efea3d537f4f96…` | `e3c7f87f48c3cae7…` |
| conservative-camera | `heartgold-english-visual-plus-conservative-camera-1.0.0.xdelta` | `2c52928390ce38a0…` | `de15acca3b941dee…` |

Source ROM (clean, user-supplied): SHA-256 `65f02a56842b75aa92d775d56d657a56fe3fa993550b04dc20704ab82d760105`

## Automated checks

| Variant | Check | Status | Detail |
|---|---|---|---|
| visual-only | patch round-trip | ✅ PASS | sha256 ad2afac2eea9… |
| visual-only | game code unchanged | ✅ PASS | IPKE |
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
| safe | patch round-trip | ✅ PASS | sha256 4d9219bee5bf… |
| safe | game code unchanged | ✅ PASS | IPKE |
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
| full | patch round-trip | ✅ PASS | sha256 e3c7f87f48c3… |
| full | game code unchanged | ✅ PASS | IPKE |
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
| conservative-camera | patch round-trip | ✅ PASS | sha256 de15acca3b94… |
| conservative-camera | game code unchanged | ✅ PASS | IPKE |
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
