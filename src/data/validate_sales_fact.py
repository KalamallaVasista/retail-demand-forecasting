from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

FACT_FILE = PROCESSED_DATA_DIR / "fact_sales.csv"

CHUNK_SIZE = 1_000_000
EXPECTED_ROWS = 59_181_090


def main() -> None:
    print("Validating M5 sales fact table...")
    print(f"Chunk size: {CHUNK_SIZE:,} rows")

    total_rows = 0
    missing_values = 0
    negative_sales = 0

    unique_items = set()
    unique_stores = set()
    unique_days = set()

    reader = pd.read_csv(
        FACT_FILE,
        chunksize=CHUNK_SIZE,
    )

    for chunk_number, chunk in enumerate(reader, start=1):

        total_rows += len(chunk)

        missing_values += int(
            chunk.isnull().sum().sum()
        )

        negative_sales += int(
            (chunk["units_sold"] < 0).sum()
        )

        unique_items.update(
            chunk["item_id"].unique()
        )

        unique_stores.update(
            chunk["store_id"].unique()
        )

        unique_days.update(
            chunk["d"].unique()
        )

        print(
            f"Chunk {chunk_number}: "
            f"{len(chunk):,} rows checked "
            f"| Total: {total_rows:,}"
        )

    assert total_rows == EXPECTED_ROWS, (
        f"Expected {EXPECTED_ROWS:,} rows, "
        f"found {total_rows:,}."
    )

    assert missing_values == 0, (
        f"Missing values found: {missing_values:,}"
    )

    assert negative_sales == 0, (
        f"Negative sales found: {negative_sales:,}"
    )

    assert len(unique_items) == 3049, (
        f"Expected 3,049 items, found {len(unique_items):,}."
    )

    assert len(unique_stores) == 10, (
        f"Expected 10 stores, found {len(unique_stores):,}."
    )

    assert len(unique_days) == 1941, (
        f"Expected 1,941 days, found {len(unique_days):,}."
    )

    print("\nSales fact validation passed.")
    print(f"Rows: {total_rows:,}")
    print(f"Unique items: {len(unique_items):,}")
    print(f"Unique stores: {len(unique_stores):,}")
    print(f"Unique days: {len(unique_days):,}")
    print(f"Missing values: {missing_values:,}")
    print(f"Negative sales: {negative_sales:,}")

    print("\nAll sales fact validation checks passed successfully.")


if __name__ == "__main__":
    main()