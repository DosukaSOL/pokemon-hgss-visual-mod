#!/usr/bin/env python3
"""Game profiles for the Visual+ English port pipeline.

Each profile identifies a supported base game by NDS game code and SHA-256,
and records where its ROM can be found locally. ROMs are never committed.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "tests" / "rom_manifest.json"


@dataclass(frozen=True)
class GameProfile:
    key: str                # e.g. "heartgold"
    title: str              # display name
    region: str             # "korean" | "usa"
    game_code: str          # NDS header game code
    manifest_role: str      # role in tests/rom_manifest.json
    supported: bool = True  # False for future games


PROFILES: dict[str, GameProfile] = {p.key: p for p in [
    GameProfile("heartgold_kor", "Pokémon HeartGold (Korea)", "korean", "IPKK",
                "korean_heartgold_clean"),
    GameProfile("soulsilver_kor", "Pokémon SoulSilver (Korea)", "korean", "IPGK",
                "korean_soulsilver_clean"),
    GameProfile("heartgold_usa", "Pokémon HeartGold (USA)", "usa", "IPKE",
                "usa_heartgold_clean"),
    GameProfile("soulsilver_usa", "Pokémon SoulSilver (USA)", "usa", "IPGE",
                "usa_soulsilver_clean"),
    # Future games — profiles reserved, not yet supported:
    GameProfile("platinum_usa", "Pokémon Platinum (USA)", "usa", "CPUE",
                "usa_platinum_clean", supported=False),
    GameProfile("diamond_usa", "Pokémon Diamond (USA)", "usa", "ADAE",
                "usa_diamond_clean", supported=False),
    GameProfile("pearl_usa", "Pokémon Pearl (USA)", "usa", "APAE",
                "usa_pearl_clean", supported=False),
    GameProfile("black_usa", "Pokémon Black (USA)", "usa", "IRBO",
                "usa_black_clean", supported=False),
    GameProfile("white_usa", "Pokémon White (USA)", "usa", "IRAO",
                "usa_white_clean", supported=False),
]}


def manifest_sha256(role: str) -> str | None:
    data = json.loads(MANIFEST.read_text())
    for entry in data["roms"]:
        if entry["role"] == role:
            return entry["sha256"]
    return None


def find_rom(profile: GameProfile) -> Path:
    """Locate the verified ROM for a profile via its manifest SHA-256."""
    import hashlib

    want = manifest_sha256(profile.manifest_role)
    if want is None:
        raise FileNotFoundError(f"no manifest entry for {profile.manifest_role}")
    search = [
        Path.home() / "Desktop" / "HGSS ROMS",
        REPO_ROOT / "local_data" / "input" / "roms",
    ]
    for d in search:
        if not d.is_dir():
            continue
        for p in sorted(d.rglob("*.nds")):
            h = hashlib.sha256()
            with p.open("rb") as f:
                for chunk in iter(lambda: f.read(1 << 20), b""):
                    h.update(chunk)
            if h.hexdigest() == want:
                return p
    raise FileNotFoundError(
        f"verified ROM for {profile.title} (sha256 {want[:12]}…) not found")
