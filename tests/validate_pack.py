#!/usr/bin/env python3
"""Static validation for the published Bedrock .mcpack package."""
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "Craftable_Dripstone_V_Recipe_1.21.60.mcpack"
SOURCE = ROOT / "pack_source"
EXPECTED = {
    "manifest.json",
    "pack_icon.png",
    "recipes/pointed_dripstone.json",
}

with zipfile.ZipFile(PACK) as archive:
    assert archive.testzip() is None, "ZIP CRC/integrity check failed"
    names = set(archive.namelist())
    assert names == EXPECTED, f"Unexpected pack contents: {sorted(names)}"
    manifest = json.loads(archive.read("manifest.json"))
    recipe = json.loads(archive.read("recipes/pointed_dripstone.json"))
    icon = archive.read("pack_icon.png")

source_manifest = json.loads((SOURCE / "manifest.json").read_text(encoding="utf-8"))
source_recipe = json.loads((SOURCE / "recipes" / "pointed_dripstone.json").read_text(encoding="utf-8"))
assert manifest == source_manifest, "Pack manifest differs from source manifest"
assert recipe == source_recipe, "Pack recipe differs from source recipe"
assert manifest["format_version"] == 2
assert manifest["header"]["min_engine_version"] == [1, 21, 60]
modules = manifest.get("modules", [])
assert len(modules) == 1 and modules[0]["type"] == "data", "Expected one behavior-pack data module"
assert manifest["header"]["uuid"] != modules[0]["uuid"], "Header and module UUIDs must differ"
assert icon.startswith(b"\x89PNG\r\n\x1a\n"), "pack_icon.png is not a PNG"

shaped = recipe["minecraft:recipe_shaped"]
assert shaped["tags"] == ["crafting_table"]
assert shaped["pattern"] == [" C ", "C C"], "Recipe must look like a V"
assert sum(row.count("C") for row in shaped["pattern"]) == 3
assert shaped["key"]["C"]["item"] == "minecraft:cobblestone"
assert shaped["result"] == {"item": "minecraft:pointed_dripstone", "count": 4}
print("PASS: valid ZIP, expected pack files, matching source JSON, behavior-pack manifest, PNG icon, 3-cobblestone V recipe -> 4 pointed dripstone")
