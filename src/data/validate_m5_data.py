from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def validate_calendar() -> None:
    """Validate the M5 calendar dataset."""

    print("\nValidating calendar.csv...")

    calendar = pd.read_csv(RAW_DATA_DIR / "calendar.csv")

    required_columns = {
        "date",
        "wm_yr_wk",
        "weekday",
        "wday",
        "month",
        "year",
        "d",
    }

    missing_columns = required_columns - set(calendar.columns)

    assert not missing_columns, (
        f"Missing calendar columns: {missing_columns}"
    )

    assert calendar["date"].notna().all(), "Missing dates found."
    assert calendar["d"].notna().all(), "Missing day identifiers found."
    assert calendar["date"].is_unique, "Duplicate dates found."
    assert calendar["d"].is_unique, "Duplicate day identifiers found."

    print(f"Rows: {len(calendar):,}")
    print("Required columns: PASS")
    print("Date completeness: PASS")
    print("Unique dates: PASS")
    print("Unique day identifiers: PASS")


def validate_sales() -> None:
    """Validate the M5 evaluation sales dataset."""

    print("\nValidating sales_train_evaluation.csv...")

    sales = pd.read_csv(
        RAW_DATA_DIR / "sales_train_evaluation.csv"
    )

    id_columns = [
        "id",
        "item_id",
        "dept_id",
        "cat_id",
        "store_id",
        "state_id",
    ]

    missing_columns = set(id_columns) - set(sales.columns)

    assert not missing_columns, (
        f"Missing sales columns: {missing_columns}"
    )

    assert sales["id"].is_unique, "Duplicate sales IDs found."

    day_columns = [
        column for column in sales.columns if column.startswith("d_")
    ]

    assert len(day_columns) == 1941, (
        f"Expected 1941 day columns, found {len(day_columns)}."
    )

    assert sales[id_columns].notna().all().all(), (
        "Missing hierarchy identifiers found."
    )

    assert sales[day_columns].notna().all().all(), (
        "Missing sales values found."
    )

    assert (sales[day_columns] >= 0).all().all(), (
        "Negative unit sales found."
    )

    print(f"Rows: {len(sales):,}")
    print(f"Day columns: {len(day_columns):,}")
    print("Unique IDs: PASS")
    print("Hierarchy completeness: PASS")
    print("Sales completeness: PASS")
    print("Non-negative sales: PASS")


def validate_prices() -> None:
    """Validate the M5 selling-price dataset."""

    print("\nValidating sell_prices.csv...")

    prices = pd.read_csv(RAW_DATA_DIR / "sell_prices.csv")

    required_columns = [
        "store_id",
        "item_id",
        "wm_yr_wk",
        "sell_price",
    ]

    assert prices[required_columns].notna().all().all(), (
        "Missing price data found."
    )

    duplicate_keys = prices.duplicated(
        subset=["store_id", "item_id", "wm_yr_wk"]
    ).sum()

    assert duplicate_keys == 0, (
        f"Duplicate price keys found: {duplicate_keys}"
    )

    assert (prices["sell_price"] > 0).all(), (
        "Zero or negative selling prices found."
    )

    print(f"Rows: {len(prices):,}")
    print("Price completeness: PASS")
    print("Unique store-item-week keys: PASS")
    print("Positive selling prices: PASS")


def main() -> None:
    print("M5 Forecasting Dataset - Data Quality Validation")

    validate_calendar()
    validate_sales()
    validate_prices()

    print("\nAll M5 data quality checks passed successfully.")


if __name__ == "__main__":
    main()