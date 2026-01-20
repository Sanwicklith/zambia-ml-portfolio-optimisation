from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class DatasetBundle:
    prices_daily: pd.DataFrame        # index=date, columns=tickers
    cpi: pd.Series                    # index=date, values=cpi
    gdp_annual: Optional[pd.Series]   # index=year-end date, values=gdp


class DataLoader:
    """
    Isolated ingestion layer.
    No feature engineering here; only clean loading and standardisation.
    """

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir

    def load_luse_prices(self, filename: str = "LuSE_Closing prices.xlsx") -> pd.DataFrame:
        path = self.data_dir / filename
        df = pd.read_excel(path)

        # Try to detect date column robustly
        date_col = None
        for c in df.columns:
            if str(c).strip().lower() in {"date", "dates", "trading date", "day"}:
                date_col = c
                break
        if date_col is None:
            # Fallback: assume first column is date
            date_col = df.columns[0]

        df[date_col] = pd.to_datetime(df[date_col])
        df = df.set_index(date_col).sort_index()

        # Keep only numeric columns (tickers)
        df = df.apply(pd.to_numeric, errors="coerce")
        df = df.loc[~df.index.duplicated(keep="first")]

        return df

    def load_cpi(self, filename: str = "Consumer Price index.xls") -> pd.Series:
        path = self.data_dir / filename
        df = pd.read_excel(path)

        # Detect date-like column
        date_col = None
        for c in df.columns:
            if str(c).strip().lower() in {"date", "month", "period"}:
                date_col = c
                break
        if date_col is None:
            date_col = df.columns[0]

        # Detect CPI column
        value_col = None
        for c in df.columns:
            if "cpi" in str(c).lower() or "index" in str(c).lower():
                value_col = c
                break
        if value_col is None:
            value_col = df.columns[-1]

        df[date_col] = pd.to_datetime(df[date_col])
        s = pd.to_numeric(df[value_col], errors="coerce")
        s.index = df[date_col]
        s = s.sort_index()
        s = s.loc[~s.index.duplicated(keep="first")]
        return s.rename("cpi")

    def load_gdp_annual(self, filename: str = "Final-Annual_GDP_2024_Zambia.xlsx") -> Optional[pd.Series]:
        path = self.data_dir / filename
        if not path.exists():
            return None

        df = pd.read_excel(path)

        # Attempt to find year and value columns
        year_col = None
        for c in df.columns:
            if str(c).strip().lower() in {"year", "yr"}:
                year_col = c
                break
        if year_col is None:
            year_col = df.columns[0]

        value_col = None
        for c in df.columns:
            lc = str(c).lower()
            if "gdp" in lc and ("constant" in lc or "current" in lc or "value" in lc):
                value_col = c
                break
        if value_col is None:
            value_col = df.columns[-1]

        years = pd.to_numeric(df[year_col], errors="coerce").astype("Int64")
        vals = pd.to_numeric(df[value_col], errors="coerce")

        s = pd.Series(vals.values, index=years.values, name="gdp")
        s = s.dropna()
        # convert to year-end dates for merging later
        idx = pd.to_datetime(s.index.astype(int).astype(str) + "-12-31")
        s.index = idx
        return s.sort_index()

    @staticmethod
    def to_monthly_last(prices_daily: pd.DataFrame) -> pd.DataFrame:
        """Convert daily prices to month-end prices (last observation)."""
        return prices_daily.resample("M").last()

    @staticmethod
    def compute_returns(prices: pd.DataFrame) -> pd.DataFrame:
        """Simple returns; can be swapped to log returns later."""
        return prices.pct_change()

    @staticmethod
    def align_monthly(
        rets_m: pd.DataFrame,
        cpi_m: pd.Series,
        gdp_a: Optional[pd.Series],
    ) -> pd.DataFrame:
        """
        Produce a single monthly panel with:
        - asset returns (columns: tickers)
        - CPI inflation (monthly % change)
        - GDP (annual, forward-filled)
        """
        cpi_m = cpi_m.resample("M").last()
        infl_m = cpi_m.pct_change().rename("inflation_m")

        out = rets_m.copy()
        out["inflation_m"] = infl_m

        if gdp_a is not None:
            gdp_m = gdp_a.resample("M").ffill().rename("gdp")
            out["gdp"] = gdp_m

        return out
