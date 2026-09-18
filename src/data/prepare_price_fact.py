from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

INPUT_FILE = RAW_DATA_DIR / "sell_prices.csv"
OUTPUT_FILE = PROCESSED_DATA_DIR / "fact_prices.csv"


def main() -> None:
    print("Preparing M5 price fact table...")

    prices = pd.read_csv(INPUT_FILE)

    fact_prices = prices[
        [
            "store_id",
            "item_id",
            "wm_yr_wk",
            "sell_price",
        ]
    ].copy()

    # Data-quality validation
    assert fact_prices.isnull().sum().sum() == 0, (
        "Missing values found in price fact table."
    )

    duplicate_keys = fact_prices.duplicated(
        subset=["store_id", "item_id", "wm_yr_wk"]
    ).sum()

    assert duplicate_keys == 0, (
        f"Duplicate store-item-week keys found: {duplicate_keys}"
    )

    assert (fact_prices["sell_price"] > 0).all(), (
        "Zero or negative selling prices found."
    )

    fact_prices = fact_prices.sort_values(
        ["store_id", "item_id", "wm_yr_wk"]
    ).reset_index(drop=True)

    fact_prices.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print("\nPrice fact table created successfully.")
    print(f"Rows: {len(fact_prices):,}")
    print(f"Items: {fact_prices['item_id'].nunique():,}")
    print(f"Stores: {fact_prices['store_id'].nunique():,}")
    print(f"Weeks: {fact_prices['wm_yr_wk'].nunique():,}")
    print(f"Minimum price: ${fact_prices['sell_price'].min():.2f}")
    print(f"Maximum price: ${fact_prices['sell_price'].max():.2f}")

    print(f"\nSaved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()