from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


def main() -> None:
    print("Preparing M5 date dimension...")

    calendar = pd.read_csv(
        RAW_DATA_DIR / "calendar.csv"
    )

    date_columns = [
        "date",
        "d",
        "wm_yr_wk",
        "weekday",
        "wday",
        "month",
        "year",
        "event_name_1",
        "event_type_1",
        "event_name_2",
        "event_type_2",
        "snap_CA",
        "snap_TX",
        "snap_WI",
    ]

    dim_date = calendar[date_columns].copy()

    dim_date["date"] = pd.to_datetime(dim_date["date"])

    # Validate date dimension
    assert dim_date["date"].is_unique, "Duplicate dates found."
    assert dim_date["d"].is_unique, "Duplicate day IDs found."
    assert dim_date["date"].notna().all(), "Missing dates found."
    assert dim_date["d"].notna().all(), "Missing day IDs found."

    dim_date = dim_date.sort_values("date").reset_index(drop=True)

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    output_path = PROCESSED_DATA_DIR / "dim_date.csv"

    dim_date.to_csv(
        output_path,
        index=False,
        date_format="%Y-%m-%d",
    )

    print("\nDate dimension created.")
    print(f"Rows: {len(dim_date):,}")
    print(f"Start date: {dim_date['date'].min().date()}")
    print(f"End date: {dim_date['date'].max().date()}")
    print(f"Unique weeks: {dim_date['wm_yr_wk'].nunique():,}")
    print(f"Event days: {dim_date['event_name_1'].notna().sum():,}")

    print("\nDate dimension saved successfully.")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()