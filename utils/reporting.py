from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

import pandas as pd


def ensure_dirs(*dirs: Path) -> None:
    """Atomic: create output directories if missing."""
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


def save_table(df: pd.DataFrame, path: Path) -> None:
    """Atomic: save a table deterministically."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=True)


def save_json(obj: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, default=str)


def save_config(config_obj: Any, path: Path) -> None:
    """Save config (dataclass) for audit trail."""
    save_json(asdict(config_obj), path)
