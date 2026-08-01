# FAQ

**Q: Do you provide ROMs?**
No. Never. You must dump your own cartridge. See [Legal](legal.md).

**Q: Which variant should I pick?**
`safe` for most players. `full` for the complete Visual+ experience
(occasional camera glitches on a few maps). `visual-only` if you only want
the new battle backgrounds. `conservative-camera` is a middle ground with a
50 % strength camera.

**Q: Does this work with the European / Japanese / Korean English-patched ROM?**
No. The patches are built against the **USA** dumps only and will refuse to
apply to anything else.

**Q: Will my existing save work?**
Yes — the mod doesn't change the save format or game code.

**Q: Can I use this with other romhacks (e.g. HGSS renewal hacks)?**
Not directly — xdelta patches require the exact clean source. Applying two
xdelta mods to the same ROM is not possible unless one is rebuilt on top of
the other.

**Q: Is SoulSilver identical to the HeartGold port?**
No. The upstream Korean mod only exists for HeartGold. We independently
verified every modified archive, overlay and executable region against the
SoulSilver USA binaries and built + tested its patches separately — see the
[SoulSilver Test Report](reports/SoulSilver_Test_Report.md).

**Q: What about Platinum?**
The upstream mod includes a Korean Platinum ("Giratina") patch. A Platinum
English port is planned — the game-profile pipeline already reserves it.

**Q: Why xdelta and not IPS/UPS?**
The DS filesystem gets rebuilt during modding, which makes IPS/UPS patches
enormous and unsafe. xdelta handles this and verifies the source checksum.

**Q: HP drains too fast for my taste — can I get backgrounds + camera without it?**
Currently `visual-only` (no camera) is the closest. Open an issue if you'd
like a `visual+camera` variant; the build pipeline supports it trivially.
