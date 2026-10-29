#!/usr/bin/env python3
"""Static validation for the published Bedrock 26.60 behavior pack."""
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "Craftable_Dripstone_V_Recipe_26.60.mcpack"
SOURCE = ROOT / "pack_source"
EXPECTED = {"manifest.json", "pack_icon.png", "recipes/pointed_dripstone.json"}

with zipfile.ZipFile(PACK) as archive:
    assert archive.testzip() is None, "ZIP CRC/integrity check failed"
    assert set(archive.namelist()) == EXPECTED, f"Unexpected files: {archive.namelist()}"
    manifest = json.loads(archive.read("manifest.json"))
    recipe = json.loads(archive.read("recipes/pointed_dripstone.json"))
    icon = archive.read("pack_icon.png")

assert manifest == json.loads((SOURCE / "manifest.json").read_text(encoding="utf-8"))
assert recipe == json.loads((SOURCE / "recipes" / "pointed_dripstone.json").read_text(encoding="utf-8"))
assert manifest["format_version"] == 2
assert manifest["header"]["min_engine_version"] == [1, 26, 60]
assert manifest["header"]["version"] == [1, 0, 3]
modules = manifest["modules"]
assert len(modules) == 1 and modules[0]["type"] == "data"
assert manifest["header"]["uuid"] != modules[0]["uuid"]
assert icon.startswith(b"\x89PNG\r\n\x1a\n"), "Icon is not a PNG"
shaped = recipe["minecraft:recipe_shaped"]
assert shaped["tags"] == ["crafting_table"]
assert shaped["pattern"] == ["C C", " C "], "Expected true V shape"
assert sum(row.count("C") for row in shaped["pattern"]) == 3
assert shaped["key"]["C"]["item"] == "minecraft:cobblestone"
assert shaped["result"] == {"item": "minecraft:pointed_dripstone", "count": 4}
print("PASS: ZIP integrity; exact package contents; source/package JSON match; Bedrock 26.60 behavior manifest; PNG icon; V recipe (3 cobblestone -> 4 pointed dripstone).")
