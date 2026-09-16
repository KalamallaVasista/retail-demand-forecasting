from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def inspect_csv(file_name: str) -> None:
    """Display basic structure and quality information for an M5 CSV file."""

    file_path = RAW_DATA_DIR / file_name

    print("\n" + "=" * 70)
    print(f"FILE: {file_name}")
    print("=" * 70)

    df = pd.read_csv(file_path)

    print(f"Shape: {df.shape}")
    print(f"Rows: {df.shape[0]:,}")
    print(f"Columns: {df.shape[1]:,}")

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nFirst 3 rows:")
    print(df.head(3))

    print("\nMissing values:")
    missing = df.isnull().sum()
    print(missing[missing > 0])

    print(f"\nDuplicate rows: {df.duplicated().sum():,}")


def main() -> None:
    print("M5 Forecasting Dataset - Initial Inspection")

    files = [
        "calendar.csv",
        "sales_train_evaluation.csv",
        "sales_train_validation.csv",
        "sell_prices.csv",
    ]

    for file_name in files:
        inspect_csv(file_name)


if __name__ == "__main__":
    main()