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


@dataclass(frozen=True)
class RunConfig:
    """
    Run configuration. Keep this stable for reproducibility and thesis traceability.
    """
    seed: int = 42
    frequency: str = "M"  # monthly
    min_history_months: int = 24
    test_months: int = 24
    forecast_horizons: tuple[int, ...] = (1, 3)  # months ahead
    risk_free_rate_annual: float = 0.0  # can be updated later

    # Portfolio constraints (frontier-market realism)
    max_weight: float = 0.20
    min_weight: float = 0.00
    allow_short: bool = False
    transaction_cost_bps: float = 20.0  # 20 bps per rebalance (placeholder)
