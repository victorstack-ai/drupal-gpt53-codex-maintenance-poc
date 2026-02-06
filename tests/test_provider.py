from __future__ import annotations

import json

from drupal_gpt53_codex_poc.models import ModuleScan
from drupal_gpt53_codex_poc.provider import OpenAIProvider


def test_openai_provider_payload_without_key(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    scan = ModuleScan(
        module_path="/tmp/example",
        module_name="Example",
        info_path=None,
        info={},
        composer_path=None,
        composer={},
        php_files=1,
        test_files=0,
        todo_count=0,
        readme_present=False,
        services_present=False,
        drush_services_present=False,
    )
    provider = OpenAIProvider()

    payload = json.loads(provider.generate(scan, [], "gpt-5.3-codex"))

    assert payload["model"] == "gpt-5.3-codex"
    assert "note" in payload
