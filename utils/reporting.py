from __future__ import annotations

import json
import os
from dataclasses import asdict
from pathlib import Path
from typing import Any

import pandas as pd


def ensure_dirs(*dirs: Path) -> None:
    """Create output directories if missing."""
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


def save_table(df: pd.DataFrame, path: Path) -> None:
    """
    Atomic: save a table deterministically as CSV.

    Writes to a temporary file in the same directory, then replaces the target.
    This prevents partially written/corrupted files if execution is interrupted.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    df.to_csv(tmp_path, index=True)
    os.replace(tmp_path, path)


def atomic_write_parquet(df: pd.DataFrame, path: Path) -> None:
    """
    Atomic: save a table deterministically as Parquet.

    Writes to a temporary file in the same directory, then replaces the target.
    This prevents partially written/corrupted files if execution is interrupted.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    df.to_parquet(tmp_path, index=False)
    os.replace(tmp_path, path)


def save_json(obj: dict[str, Any], path: Path) -> None:
    """Save a JSON file (non-atomic)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, default=str)


def save_config(config_obj: Any, path: Path) -> None:
    """Save config (dataclass) for audit trail."""
    save_json(asdict(config_obj), path)
