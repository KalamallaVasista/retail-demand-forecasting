from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


def main() -> None:
    print("Preparing M5 dimension tables...")

    sales = pd.read_csv(
        RAW_DATA_DIR / "sales_train_evaluation.csv",
        usecols=[
            "item_id",
            "dept_id",
            "cat_id",
            "store_id",
            "state_id",
        ],
    )

    # Product hierarchy: item -> department -> category
    products = (
        sales[["item_id", "dept_id", "cat_id"]]
        .drop_duplicates()
        .sort_values("item_id")
        .reset_index(drop=True)
    )

    # Store hierarchy: store -> state
    stores = (
        sales[["store_id", "state_id"]]
        .drop_duplicates()
        .sort_values("store_id")
        .reset_index(drop=True)
    )

    # Validate hierarchy
    assert products["item_id"].is_unique
    assert stores["store_id"].is_unique

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    products.to_csv(
        PROCESSED_DATA_DIR / "dim_product.csv",
        index=False,
    )

    stores.to_csv(
        PROCESSED_DATA_DIR / "dim_store.csv",
        index=False,
    )

    print("\nProduct dimension created.")
    print(f"Products: {len(products):,}")
    print(f"Departments: {products['dept_id'].nunique()}")
    print(f"Categories: {products['cat_id'].nunique()}")

    print("\nStore dimension created.")
    print(f"Stores: {len(stores)}")
    print(f"States: {stores['state_id'].nunique()}")

    print("\nDimension tables saved successfully.")
    print(f"Location: {PROCESSED_DATA_DIR}")


if __name__ == "__main__":
    main()