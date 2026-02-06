from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path

import yaml

from .models import ModuleScan

IGNORED_DIRS = {".git", ".venv", "node_modules", "vendor", "dist", "build"}
TEXT_EXTENSIONS = {".php", ".yml", ".yaml", ".md", ".txt"}


def _walk_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        if path.is_file():
            yield path


def _find_info_file(root: Path) -> Path | None:
    for path in root.glob("*.info.yml"):
        return path
    return None


def _read_yaml(path: Path | None) -> dict:
    if not path or not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _read_json(path: Path | None) -> dict:
    if not path or not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def scan_module(module_path: str) -> ModuleScan:
    root = Path(module_path).resolve()
    info_path = _find_info_file(root)
    info = _read_yaml(info_path)
    module_name = info.get("name") if info else None

    composer_path = root / "composer.json"
    composer = _read_json(composer_path) if composer_path.exists() else {}
    composer_path_str = str(composer_path) if composer_path.exists() else None

    php_files = 0
    test_files = 0
    todo_count = 0

    for file_path in _walk_files(root):
        if file_path.suffix == ".php":
            php_files += 1
            if "tests" in file_path.parts or "Tests" in file_path.parts:
                test_files += 1
        if file_path.suffix.lower() in TEXT_EXTENSIONS:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            todo_count += content.count("TODO") + content.count("FIXME")

    readme_present = (root / "README.md").exists()
    services_present = any(root.glob("*.services.yml"))
    drush_services_present = (root / "drush.services.yml").exists()

    return ModuleScan(
        module_path=str(root),
        module_name=module_name,
        info_path=str(info_path) if info_path else None,
        info=info,
        composer_path=composer_path_str,
        composer=composer,
        php_files=php_files,
        test_files=test_files,
        todo_count=todo_count,
        readme_present=readme_present,
        services_present=services_present,
        drush_services_present=drush_services_present,
    )
