# Compatibility Matrix

Each game is tracked **independently** — results for one game are never
assumed to apply to the other.

## HeartGold (English Visual+)

Source ROM: *Pokémon HeartGold Version (USA)*, game code `IPKE`,
SHA-256 `65f02a56842b75aa92d775d56d657a56fe3fa993550b04dc20704ab82d760105`

### Automated validation

| Check | visual-only | safe | full | conservative-camera |
|---|---|---|---|---|
| Patch round-trip (xdelta3) | ✅ | ✅ | ✅ | ✅ |
| Header / title / banner intact | ✅ | ✅ | ✅ | ✅ |
| 73 map battle-bg IDs | ✅ | ✅ | ✅ | ✅ |
| arm9 cave + hook + uncompressed | ✅ | ✅ | ✅ | ✅ |
| Overlay 1 (visual byte + camera) | ✅ | ✅ | ✅ | ✅ |
| Overlay 12 (HP speed) | ✅ (clean) | ✅ | ✅ | ✅ |
| NARC subfiles (a/0/0/7, a/0/0/8, a/2/6/2) | ✅ | ✅ | ✅ | ✅ |
| Isolation sweep (513 files) | ✅ | ✅ | ✅ | ✅ |

### Platforms

| Platform | visual-only | safe | full | conservative-camera |
|---|---|---|---|---|
| melonDS (desktop) | 🟡 untested | 🟡 untested | ✅ boots, intro OK | 🟡 untested |
| melonDS (Android / AYN Thor) | 🟡 untested | 🟡 untested | 🟡 untested | 🟡 untested |
| DeSmuME | 🟡 untested | 🟡 untested | 🟡 untested | 🟡 untested |
| DraStic | 🟡 untested | 🟡 untested | 🟡 untested | 🟡 untested |
| Real hardware (flashcart) | 🟡 untested | 🟡 untested | 🟡 untested | 🟡 untested |

Full details: [HeartGold Test Report](reports/HeartGold_Test_Report.md)

---

## SoulSilver (English Visual+)

Source ROM: *Pokémon SoulSilver Version (USA)*, game code `IPGE`,
SHA-256 `51d0f94a16af7d77c067b4cb7d821ba890a13203a2e2c76049623332c0582e20`

### Automated validation

| Check | visual-only | safe | full | conservative-camera |
|---|---|---|---|---|
| Patch round-trip (xdelta3) | ✅ | ✅ | ✅ | ✅ |
| Header / title / banner intact | ✅ | ✅ | ✅ | ✅ |
| 73 map battle-bg IDs | ✅ | ✅ | ✅ | ✅ |
| arm9 cave + hook + uncompressed | ✅ | ✅ | ✅ | ✅ |
| Overlay 1 (visual byte + camera) | ✅ | ✅ | ✅ | ✅ |
| Overlay 12 (HP speed) | ✅ (clean) | ✅ | ✅ | ✅ |
| NARC subfiles (a/0/0/7, a/0/0/8, a/2/6/2) | ✅ | ✅ | ✅ | ✅ |
| Isolation sweep (513 files) | ✅ | ✅ | ✅ | ✅ |

### Platforms

| Platform | visual-only | safe | full | conservative-camera |
|---|---|---|---|---|
| melonDS (desktop) | 🟡 untested | 🟡 untested | 🟡 untested | 🟡 untested |
| melonDS (Android / AYN Thor) | 🟡 untested | 🟡 untested | 🟡 untested | 🟡 untested |
| DeSmuME | 🟡 untested | 🟡 untested | 🟡 untested | 🟡 untested |
| DraStic | 🟡 untested | 🟡 untested | 🟡 untested | 🟡 untested |
| Real hardware (flashcart) | 🟡 untested | 🟡 untested | 🟡 untested | 🟡 untested |

Full details: [SoulSilver Test Report](reports/SoulSilver_Test_Report.md)

---

Legend: ✅ verified · 🟡 untested (community reports welcome —
[Report a Bug](report-a-bug.md)) · ❌ broken
