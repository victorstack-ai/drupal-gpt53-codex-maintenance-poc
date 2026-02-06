from __future__ import annotations

from pathlib import Path

from drupal_gpt53_codex_poc.analysis import build_findings
from drupal_gpt53_codex_poc.scanner import scan_module


def _build_module(root: Path) -> None:
    (root / "example.info.yml").write_text("name: Example\n", encoding="utf-8")


def test_findings_include_missing_core_version(tmp_path: Path) -> None:
    _build_module(tmp_path)

    scan = scan_module(str(tmp_path))
    findings = build_findings(scan)

    messages = {finding.message for finding in findings}
    assert "Missing core_version_requirement in .info.yml." in messages
