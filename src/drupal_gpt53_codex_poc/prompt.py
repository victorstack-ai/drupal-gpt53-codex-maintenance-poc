from __future__ import annotations

import json

from .models import Finding, ModuleScan


def build_prompt(scan: ModuleScan, findings: list[Finding]) -> str:
    summary = {
        "module_name": scan.module_name,
        "module_path": scan.module_path,
        "core_version_requirement": scan.info.get("core_version_requirement"),
        "dependencies": scan.info.get("dependencies", []),
        "php_files": scan.php_files,
        "test_files": scan.test_files,
        "todo_count": scan.todo_count,
        "readme_present": scan.readme_present,
        "composer_present": bool(scan.composer_path),
    }
    findings_payload = [
        {"severity": finding.severity, "message": finding.message, "evidence": finding.evidence}
        for finding in findings
    ]

    return "\n".join(
        [
            "You are GPT-5.3-Codex, acting as a Drupal module maintenance agent.",
            "Review the module scan summary and findings, then produce:",
            "1) A prioritized maintenance plan (high/medium/low)",
            "2) Concrete code-level tasks with file targets",
            "3) A quick risk assessment for Drupal 11+ compatibility",
            "4) Suggested tests to add or update",
            "",
            "Module Scan Summary (JSON):",
            json.dumps(summary, indent=2, sort_keys=True),
            "",
            "Findings (JSON):",
            json.dumps(findings_payload, indent=2, sort_keys=True),
        ]
    )
