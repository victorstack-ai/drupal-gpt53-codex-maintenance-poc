# Drupal GPT-5.3 Codex Maintenance POC

Proof-of-concept CLI that scans a Drupal module and produces a maintenance brief plus a GPT-5.3-Codex-ready prompt. It does not require external services by default. When `--provider openai` is used, the tool will validate environment configuration and show the prepared request payload without sending it (POC safety).

## Why

Drupal module maintenance work benefits from consistent checklists and evidence. This POC:

- extracts module metadata (`.info.yml`, `composer.json`)
- inspects basic structure (tests, services, README)
- finds TODO/FIXME markers
- builds a prompt suitable for a GPT-5.3-Codex agent

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

```bash
# Text report + prompt
python -m drupal_gpt53_codex_poc analyze /path/to/module

# JSON output
python -m drupal_gpt53_codex_poc analyze /path/to/module --format json

# Emit prompt only
python -m drupal_gpt53_codex_poc analyze /path/to/module --emit-prompt

# POC openai provider (prints payload, does not send)
python -m drupal_gpt53_codex_poc analyze /path/to/module --provider openai
```

## Output

The report includes:

- core version requirement
- declared dependencies
- test and PHP file counts
- TODO/FIXME markers
- missing docs or config files

## Notes

This is a POC. The `openai` provider is intentionally non-networked for safety and repeatability in tests.
