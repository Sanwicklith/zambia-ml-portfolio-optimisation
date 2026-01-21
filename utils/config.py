from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Paths:
    """Centralised, consistent paths (no hardcoding in modules)."""
    project_root: Path

    @property
    def data_dir(self) -> Path:
        return self.project_root / "data_analysis"

    @property
    def outputs_dir(self) -> Path:
        return self.project_root / "outputs"

    @property
    def tables_dir(self) -> Path:
        return self.outputs_dir / "tables"

    @property
    def figures_dir(self) -> Path:
        return self.outputs_dir / "figures"

    @property
    def models_dir(self) -> Path:
        return self.outputs_dir / "models"

    @property
    def logs_dir(self) -> Path:
        return self.outputs_dir / "logs"

    # ---- LuSE-specific paths ----

    @property
    def raw_luse_xlsx(self) -> Path:
        return self.data_dir / "LuSE_Closing prices.xlsx"

    @property
    def prices_daily_long_path(self) -> Path:
        return self.tables_dir / "luse_prices_daily_long.parquet"

    @property
    def prices_monthly_path(self) -> Path:
        return self.tables_dir / "luse_prices_monthly.parquet"

    @property
    def returns_monthly_panel_path(self) -> Path:
        return self.tables_dir / "luse_returns_monthly.parquet"

    def ensure_dirs(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.outputs_dir.mkdir(parents=True, exist_ok=True)
        self.tables_dir.mkdir(parents=True, exist_ok=True)
        self.figures_dir.mkdir(parents=True, exist_ok=True)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)


@dataclass(frozen=True)
class RunConfig:
    """
    Run configuration. Keep this stable for reproducibility and thesis traceability.
    """
    seed: int = 42
    frequency: str = "M"  # monthly
    min_history_months: int = 24
    test_months: int = 24
    forecast_horizons: tuple[int, ...] = (1, 3)
    risk_free_rate_annual: float = 0.0

    # Portfolio constraints (frontier-market realism)
    max_weight: float = 0.20
    min_weight: float = 0.00
    allow_short: bool = False
    transaction_cost_bps: float = 20.0
