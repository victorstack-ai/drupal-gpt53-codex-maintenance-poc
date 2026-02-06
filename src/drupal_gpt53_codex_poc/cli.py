from __future__ import annotations

import argparse
import json

from .analysis import build_findings
from .prompt import build_prompt
from .provider import resolve_provider
from .scanner import scan_module


def _render_text(scan, findings, provider_output, emit_prompt: bool) -> str:
    lines = [
        f"Module: {scan.module_name or 'Unknown'}",
        f"Path: {scan.module_path}",
        f"Info file: {scan.info_path or 'Missing'}",
        f"Composer: {scan.composer_path or 'Missing'}",
        f"PHP files: {scan.php_files}",
        f"Test files: {scan.test_files}",
        f"TODO/FIXME markers: {scan.todo_count}",
        f"README: {'yes' if scan.readme_present else 'no'}",
        "",
        "Findings:",
    ]

    if findings:
        for finding in findings:
            lines.append(f"- [{finding.severity}] {finding.message}")
    else:
        lines.append("- none")

    lines.extend(["", "Provider Output:", provider_output])

    if emit_prompt:
        lines.extend(["", "Prompt:", build_prompt(scan, findings)])

    return "\n".join(lines)


def _render_json(scan, findings, provider_output, emit_prompt: bool) -> str:
    payload = {
        "scan": {
            "module_name": scan.module_name,
            "module_path": scan.module_path,
            "info_path": scan.info_path,
            "composer_path": scan.composer_path,
            "php_files": scan.php_files,
            "test_files": scan.test_files,
            "todo_count": scan.todo_count,
            "readme_present": scan.readme_present,
        },
        "findings": [
            {"severity": f.severity, "message": f.message, "evidence": f.evidence}
            for f in findings
        ],
        "provider_output": provider_output,
    }
    if emit_prompt:
        payload["prompt"] = build_prompt(scan, findings)
    return json.dumps(payload, indent=2, sort_keys=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="drupal-gpt53-codex")
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser("analyze", help="Analyze a Drupal module")
    analyze.add_argument("module_path")
    analyze.add_argument("--format", choices=["text", "json"], default="text")
    analyze.add_argument("--provider", choices=["mock", "openai"], default="mock")
    analyze.add_argument("--model", default="gpt-5.3-codex")
    analyze.add_argument("--emit-prompt", action="store_true")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    scan = scan_module(args.module_path)
    findings = build_findings(scan)
    provider = resolve_provider(args.provider)
    provider_output = provider.generate(scan, findings, args.model)

    if args.format == "json":
        print(_render_json(scan, findings, provider_output, args.emit_prompt))
    else:
        print(_render_text(scan, findings, provider_output, args.emit_prompt))


if __name__ == "__main__":
    main()
