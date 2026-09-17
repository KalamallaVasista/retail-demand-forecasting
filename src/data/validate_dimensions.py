from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


def main() -> None:
    print("Validating M5 dimension tables...")

    products = pd.read_csv(
        PROCESSED_DATA_DIR / "dim_product.csv"
    )

    stores = pd.read_csv(
        PROCESSED_DATA_DIR / "dim_store.csv"
    )

    dates = pd.read_csv(
        PROCESSED_DATA_DIR / "dim_date.csv"
    )

    # Product dimension
    assert len(products) == 3049, "Unexpected product count."
    assert products["item_id"].is_unique, "Duplicate item IDs found."
    assert products.isnull().sum().sum() == 0, (
        "Missing product hierarchy values found."
    )

    # Store dimension
    assert len(stores) == 10, "Unexpected store count."
    assert stores["store_id"].is_unique, "Duplicate store IDs found."
    assert stores.isnull().sum().sum() == 0, (
        "Missing store hierarchy values found."
    )

    # Date dimension
    assert len(dates) == 1969, "Unexpected date count."
    assert dates["date"].is_unique, "Duplicate dates found."
    assert dates["d"].is_unique, "Duplicate day IDs found."

    print("\nProduct dimension: PASS")
    print(f"Products: {len(products):,}")
    print(f"Departments: {products['dept_id'].nunique()}")
    print(f"Categories: {products['cat_id'].nunique()}")

    print("\nStore dimension: PASS")
    print(f"Stores: {len(stores)}")
    print(f"States: {stores['state_id'].nunique()}")

    print("\nDate dimension: PASS")
    print(f"Dates: {len(dates):,}")
    print(f"Weeks: {dates['wm_yr_wk'].nunique():,}")

    print("\nAll dimension validation checks passed successfully.")


if __name__ == "__main__":
    main()