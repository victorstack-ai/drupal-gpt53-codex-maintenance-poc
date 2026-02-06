from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ModuleScan:
    module_path: str
    module_name: str | None
    info_path: str | None
    info: dict[str, Any]
    composer_path: str | None
    composer: dict[str, Any]
    php_files: int
    test_files: int
    todo_count: int
    readme_present: bool
    services_present: bool
    drush_services_present: bool


@dataclass
class Finding:
    severity: str
    message: str
    evidence: list[str] = field(default_factory=list)
