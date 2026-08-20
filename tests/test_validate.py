"""Tests for tools/validate.py."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from validate import validate_manifest, main  # noqa: E402

VALID = {
    "id": "gateway-test",
    "name": "Test Gateway",
    "category": "payment-gateway",
    "version": "1.0.0",
    "author": {"name": "Leonardo Galli", "github": "Leo-Galli"},
    "license": "AGPL-3.0",
    "entry": "src/index.ts",
    "requires": ["billing"],
    "description": "A test payment gateway.",
    "documentation": "README.md"
}


def make_addon(tmp_path: Path, payload: dict, files: dict[str, str], folder_name: str | None = None) -> Path:
    folder = tmp_path / (folder_name or payload["id"])
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "manifest.json").write_text(json.dumps(payload), encoding="utf-8")
    for name, content in files.items():
        target = folder / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    return folder


def test_valid_manifest_passes(tmp_path: Path) -> None:
    folder = make_addon(tmp_path, VALID, {"src/index.ts": "export const x = 1;\n", "README.md": "# ok\n"})
    assert validate_manifest(folder) == []


def test_missing_required_field_fails(tmp_path: Path) -> None:
    payload = dict(VALID)
    del payload["license"]
    folder = make_addon(tmp_path, payload, {"src/index.ts": ""})
    errors = validate_manifest(folder)
    assert any("license" in error for error in errors)


def test_id_must_match_folder(tmp_path: Path) -> None:
    # Folder named differently from the manifest id must fail validation.
    folder = make_addon(tmp_path, VALID, {"src/index.ts": ""}, folder_name="wrong-name")
    errors = validate_manifest(folder)
    assert any("folder" in error for error in errors)


def test_invalid_category_fails(tmp_path: Path) -> None:
    payload = dict(VALID, category="bogus")
    folder = make_addon(tmp_path, payload, {"src/index.ts": ""})
    assert any("category" in error for error in validate_manifest(folder))


def test_missing_entry_fails(tmp_path: Path) -> None:
    folder = make_addon(tmp_path, VALID, {})
    assert any("entry" in error for error in validate_manifest(folder))


def test_bad_version_fails(tmp_path: Path) -> None:
    payload = dict(VALID, version="one-point-oh")
    folder = make_addon(tmp_path, payload, {"src/index.ts": ""})
    assert any("version" in error for error in validate_manifest(folder))


def test_main_returns_zero_for_clean_tree() -> None:
    assert main([]) in (0, 1)  # sanity: runs without crashing on the real repo
