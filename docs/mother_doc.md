# Zambia ML Portfolio Optimisation – Design Notes

## Purpose
This document records design and modelling decisions for the empirical analysis
supporting the MSc/MBA thesis on ML-based portfolio optimisation in Zambia.

---

## Data Sources
- LuSE daily closing prices (2010–2025)
- CPI (ZamStats)
- GDP (ZamStats)
- Bank of Zambia Monthly Bulletin
- SEC Q1 & Q2 2025 Media Briefs

---

## Frequency Choice
Monthly frequency chosen due to:
- LuSE liquidity constraints
- Reduction of microstructure noise
- Alignment with macro data release cycles

---

## Models Implemented
- Random Forest (baseline non-linear model)
- XGBoost (gradient-boosted trees)
- LSTM (only if serial dependence justified)

---

## Benchmarks
- Mean–Variance (Markowitz)
- Black–Litterman

---

## Performance Metrics
Primary:
- Sortino Ratio

Secondary:
- Sharpe Ratio
- Maximum Drawdown
- Turnover

---

## Mapping to Thesis
- Chapter 3: Methodology → code structure
- Chapter 4: Results → outputs/tables
- Chapter 5: Discussion → interpretation of results
