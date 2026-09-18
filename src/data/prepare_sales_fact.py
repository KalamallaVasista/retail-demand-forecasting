from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

INPUT_FILE = RAW_DATA_DIR / "sales_train_evaluation.csv"
OUTPUT_FILE = PROCESSED_DATA_DIR / "fact_sales.csv"

CHUNK_SIZE = 500


def main() -> None:
    print("Preparing M5 sales fact table...")
    print(f"Chunk size: {CHUNK_SIZE} series")

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    if OUTPUT_FILE.exists():
        OUTPUT_FILE.unlink()

    id_columns = [
        "item_id",
        "store_id",
    ]

    first_chunk = True
    total_output_rows = 0

    reader = pd.read_csv(
        INPUT_FILE,
        chunksize=CHUNK_SIZE,
    )

    for chunk_number, chunk in enumerate(reader, start=1):

        day_columns = [
            column
            for column in chunk.columns
            if column.startswith("d_")
        ]

        fact_chunk = chunk.melt(
            id_vars=id_columns,
            value_vars=day_columns,
            var_name="d",
            value_name="units_sold",
        )

        fact_chunk.to_csv(
            OUTPUT_FILE,
            mode="w" if first_chunk else "a",
            header=first_chunk,
            index=False,
        )

        rows_written = len(fact_chunk)
        total_output_rows += rows_written

        print(
            f"Chunk {chunk_number}: "
            f"{rows_written:,} rows written "
            f"| Total: {total_output_rows:,}"
        )

        first_chunk = False

    print("\nSales fact table created successfully.")
    print(f"Total rows: {total_output_rows:,}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()