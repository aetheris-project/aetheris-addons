"""Aetheris addon manifest validator.

Checks every manifest under addons/ against the schema in docs/manifest-schema.md
and verifies that store.json lists exactly the accepted modules.

Usage:
    python tools/validate.py                 # validate everything
    python tools/validate.py addons/<id>     # validate a single addon
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADDONS_DIR = ROOT / "addons"
STORE_FILE = ROOT / "store.json"

CATEGORIES = {"payment-gateway", "notification", "storage", "utility", "panel"}
ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")

REQUIRED = {
    "id": (str, lambda v: bool(ID_RE.match(v))),
    "name": (str, lambda v: len(v) > 0),
    "category": (str, lambda v: v in CATEGORIES),
    "version": (str, lambda v: bool(VERSION_RE.match(v))),
    "author": (dict, lambda v: isinstance(v.get("name"), str) and isinstance(v.get("github"), str)),
    "license": (str, lambda v: len(v) > 0),
    "entry": (str, lambda v: len(v) > 0),
    "description": (str, lambda v: len(v) > 0),
}

OPTIONAL = {"requires": (list, lambda v: all(isinstance(x, str) for x in v)),
            "documentation": (str, lambda v: len(v) > 0)}


def validate_manifest(path: Path) -> list[str]:
    """Validate one addon folder. Returns a list of error messages."""
    errors: list[str] = []
    manifest_path = path / "manifest.json"

    if not manifest_path.exists():
        return [f"{path.name}: missing manifest.json"]

    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as cause:
        return [f"{path.name}: manifest.json is not valid JSON: {cause}"]

    if not isinstance(data, dict):
        return [f"{path.name}: manifest.json must be an object"]

    # id must match the folder name (kebab-case).
    folder_id = path.name
    if data.get("id") != folder_id:
        errors.append(f"{path.name}: manifest id '{data.get('id')}' != folder name '{folder_id}'")

    for key, (expected_type, check) in REQUIRED.items():
        value = data.get(key)
        if value is None:
            errors.append(f"{path.name}: missing required field '{key}'")
            continue
        if not isinstance(value, expected_type) or not check(value):
            errors.append(f"{path.name}: invalid field '{key}'")

    for key, (expected_type, check) in OPTIONAL.items():
        value = data.get(key)
        if value is None:
            continue
        if not isinstance(value, expected_type) or not check(value):
            errors.append(f"{path.name}: invalid optional field '{key}'")

    # The entry point must exist relative to the addon folder.
    entry = data.get("entry")
    if isinstance(entry, str) and entry:
        entry_path = path / entry
        if not entry_path.exists():
            errors.append(f"{path.name}: entry '{entry}' does not exist")

    documentation = data.get("documentation")
    if isinstance(documentation, str) and documentation:
        doc_path = path / documentation
        if not doc_path.exists():
            errors.append(f"{path.name}: documentation '{documentation}' does not exist")

    return errors


def load_store() -> list[dict]:
    """Load the store registry as a list of addon entries."""
    if not STORE_FILE.exists():
        return []
    data = json.loads(STORE_FILE.read_text(encoding="utf-8"))
    return data.get("addons", [])


def main(argv: list[str]) -> int:
    targets = [Path(arg) for arg in argv[1:]] or sorted(ADDONS_DIR.iterdir())
    errors: list[str] = []

    manifests: dict[str, dict] = {}
    for target in targets:
        if not target.is_dir():
            print(f"skipping non-directory: {target}")
            continue
        found = validate_manifest(target)
        errors.extend(found)
        manifest_path = target / "manifest.json"
        if manifest_path.exists():
            manifests[target.name] = json.loads(manifest_path.read_text(encoding="utf-8"))

    # Cross-check against the store registry.
    store = load_store()
    store_ids = {entry.get("id") for entry in store}
    manifest_ids = set(manifests)

    for missing in sorted(manifest_ids - store_ids):
        errors.append(f"store.json: missing entry for accepted addon '{missing}'")
    for stale in sorted(store_ids - manifest_ids):
        errors.append(f"store.json: entry '{stale}' has no addon folder")

    if errors:
        print("validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"validated {len(manifests)} addons and store.json: all good")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
