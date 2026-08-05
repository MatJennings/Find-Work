#!/usr/bin/env python3
"""Add a fresh Codex cache token to the local plugin version."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    manifest = Path(__file__).resolve().parents[1] / ".codex-plugin" / "plugin.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    base = str(data["version"]).split("+", 1)[0]
    token = datetime.now(timezone.utc).strftime("local-%Y%m%d-%H%M%S")
    data["version"] = f"{base}+codex.{token}"
    manifest.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(data["version"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
