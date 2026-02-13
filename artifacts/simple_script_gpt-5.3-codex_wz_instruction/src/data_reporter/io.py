from __future__ import annotations

from pathlib import Path

import pandas as pd

from .errors import UserInputError


def read_and_validate_csv(path: Path) -> pd.DataFrame:
    """Read and validate CSV input.

    Expected columns:
      - date: YYYY-MM-DD
      - value: numeric
    """
    if not path.exists():
        raise UserInputError(f"Input file not found: {path}")

    try:
        df = pd.read_csv(path)
    except Exception as exc:  # noqa: BLE001 - provide user-facing context
        raise UserInputError(f"Failed to read CSV: {path}") from exc

    missing = {c for c in ("date", "value") if c not in df.columns}
    if missing:
        raise UserInputError(
            f"Missing required column(s): {', '.join(sorted(missing))}"
        )

    try:
        df = df[["date", "value"]].copy()
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="raise")
        df["value"] = pd.to_numeric(df["value"], errors="raise")
    except Exception as exc:  # noqa: BLE001 - provide user-facing context
        raise UserInputError("Failed to parse 'date' or 'value' columns") from exc

    if df.empty:
        raise UserInputError("Input CSV contains no rows")

    if df["date"].isna().any() or df["value"].isna().any():
        raise UserInputError("'date' or 'value' contains missing values")

    df = df.sort_values("date", ascending=True, kind="mergesort").reset_index(drop=True)
    return df
