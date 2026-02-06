from __future__ import annotations

import json
import os
from typing import Protocol

from .models import Finding, ModuleScan
from .prompt import build_prompt


class Provider(Protocol):
    def generate(self, scan: ModuleScan, findings: list[Finding], model: str) -> str:
        ...


class MockProvider:
    def generate(self, scan: ModuleScan, findings: list[Finding], model: str) -> str:
        lines = [f"Model: {model}", "Maintenance plan:"]
        for finding in findings:
            lines.append(f"- [{finding.severity}] {finding.message}")
        if not findings:
            lines.append("- [low] No immediate issues detected. Review for updates.")
        return "\n".join(lines)


class OpenAIProvider:
    """POC provider that prints the request payload without sending network calls."""

    def generate(self, scan: ModuleScan, findings: list[Finding], model: str) -> str:
        api_key = os.getenv("OPENAI_API_KEY")
        prompt = build_prompt(scan, findings)
        payload = {
            "model": model,
            "input": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": prompt,
                        }
                    ],
                }
            ],
        }
        if not api_key:
            payload["note"] = "OPENAI_API_KEY missing. Payload shown without send."
        return json.dumps(payload, indent=2, sort_keys=True)


def resolve_provider(name: str) -> Provider:
    if name == "openai":
        return OpenAIProvider()
    return MockProvider()
