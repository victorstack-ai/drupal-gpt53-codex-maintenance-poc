from __future__ import annotations

from .models import Finding, ModuleScan


def build_findings(scan: ModuleScan) -> list[Finding]:
    findings: list[Finding] = []

    if not scan.info_path:
        findings.append(
            Finding(
                severity="high",
                message="Missing .info.yml file.",
                evidence=[scan.module_path],
            )
        )
    else:
        core_req = scan.info.get("core_version_requirement")
        if not core_req:
            findings.append(
                Finding(
                    severity="high",
                    message="Missing core_version_requirement in .info.yml.",
                    evidence=[scan.info_path],
                )
            )

    if not scan.composer_path:
        findings.append(
            Finding(
                severity="medium",
                message="Missing composer.json for dependency metadata.",
                evidence=[scan.module_path],
            )
        )

    if scan.test_files == 0:
        findings.append(
            Finding(
                severity="medium",
                message="No test files detected.",
                evidence=[scan.module_path],
            )
        )

    if not scan.readme_present:
        findings.append(
            Finding(
                severity="low",
                message="README.md missing (docs gap).",
                evidence=[scan.module_path],
            )
        )

    if scan.todo_count > 0:
        findings.append(
            Finding(
                severity="low",
                message=f"Found {scan.todo_count} TODO/FIXME markers.",
                evidence=[scan.module_path],
            )
        )

    return findings
