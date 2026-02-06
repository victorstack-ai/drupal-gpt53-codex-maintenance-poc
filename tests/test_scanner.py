from __future__ import annotations

import json
from pathlib import Path

import pytest

from drupal_gpt53_codex_poc.analysis import build_findings
from drupal_gpt53_codex_poc.provider import OpenAIProvider
from drupal_gpt53_codex_poc.scanner import scan_module


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _basic_module(tmp_path: Path) -> Path:
    module_dir = tmp_path / "example_module"
    module_dir.mkdir()
    _write(
        module_dir / "example_module.info.yml",
        "name: Example Module\ncore_version_requirement: ^10 || ^11\ndependencies: []\n",
    )
    _write(module_dir / "composer.json", json.dumps({"name": "example/module"}))
    _write(module_dir / "README.md", "Example")
    _write(module_dir / "src" / "Example.php", "<?php\n// TODO: update\n")
    _write(module_dir / "tests" / "src" / "ExampleTest.php", "<?php\n")
    return module_dir


def test_scan_module_counts(tmp_path: Path) -> None:
    module_dir = _basic_module(tmp_path)
    scan = scan_module(str(module_dir))

    assert scan.info_path is not None
    assert scan.php_files == 2
    assert scan.test_files == 1
    assert scan.todo_count == 1
    assert scan.readme_present is True


def test_findings_missing_core_requirement(tmp_path: Path) -> None:
    module_dir = tmp_path / "module_without_core"
    module_dir.mkdir()
    _write(module_dir / "module_without_core.info.yml", "name: Missing Core\n")

    scan = scan_module(str(module_dir))
    findings = build_findings(scan)

    assert any(
        finding.severity == "high" and "core_version_requirement" in finding.message
        for finding in findings
    )


def test_openai_provider_payload(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    module_dir = _basic_module(tmp_path)
    scan = scan_module(str(module_dir))
    findings = build_findings(scan)

    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    provider = OpenAIProvider()
    payload = provider.generate(scan, findings, "gpt-5.3-codex")

    assert "OPENAI_API_KEY missing" in payload
