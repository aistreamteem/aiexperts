"""Classifier cases for the Product Manager rules hook."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / ".claude" / "hooks" / "inject_rules_on_action.py"


def _load():
    spec = importlib.util.spec_from_file_location("inject_rules_on_action", HOOK)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load rules hook")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    mod = _load()
    cases = [
        ("Write", "docs/discovery/notes.md", "", ["discovery:note", "write:doc"]),
        ("Write", "docs/roadmap/now.md", "", ["roadmap:update", "write:doc"]),
        ("Write", "docs/prioritization/cut.md", "", ["prioritization:decide", "write:doc"]),
        ("Write", "docs/stakeholders/list.md", "", ["stakeholder:update", "write:doc"]),
        ("Write", "docs/metrics/review.md", "", ["metric:review", "write:doc"]),
        ("Write", "docs/plan/operating-plan.md", "", ["write:doc"]),
        ("Write", "docs/diagrams/index.html", "", ["write:doc"]),
        ("Bash", "", "npm run build --config webpack.js", []),
    ]
    for tool, path, command, expected in cases:
        got = mod.classify(tool, path, command)
        if got != expected:
            raise SystemExit(f"{tool} {path or command}: expected {expected}, got {got}")
    missing = [token for token in ("write:doc", "discovery:note") if token not in mod.KNOWN_TOKENS]
    if missing:
        raise SystemExit(f"KNOWN_TOKENS missing {missing}")
    print("claude rules hook tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
