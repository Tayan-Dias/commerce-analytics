import csv
import json
from collections import defaultdict
from pathlib import Path

from etl_core import (
    FILE_CONFIG,
    REJECTED_ROW_FIELDS,
    add_rejections,
    build_data_quality_report,
    build_metrics,
    process_source_rows,
    reject_conflicting_inventory_products,
    validate_foreign_keys,
    validate_inventory,
    validate_product_categories,
    validate_products,
    validate_sales,
)


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
BASE_VALIDATORS = {
    "products.csv": validate_products,
    "sales.csv": validate_sales,
    "inventory.csv": validate_inventory,
}


def read_csv_file(path):
    rows = []

    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            rows.append({key: (value or "").strip() for key, value in row.items()})

    return rows


def write_csv_file(path, fieldnames, rows):
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json_file(path, payload):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)


def ensure_output_directory():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def load_raw_rows():
    raw_rows_by_file = {}
    file_stats = {}

    for source_file in FILE_CONFIG:
        rows = read_csv_file(RAW_DIR / source_file)
        raw_rows_by_file[source_file] = rows
        file_stats[source_file] = {
            "rows_read": len(rows),
            "rows_clean": 0,
            "rows_rejected": 0,
            "duplicates_removed": 0,
        }

    return raw_rows_by_file, file_stats


def process_base_files(raw_rows_by_file, file_stats, rejected_rows, rejection_counts):
    clean_rows_by_file = {}

    for source_file, config in FILE_CONFIG.items():
        rows, source_rejections, duplicates_removed = process_source_rows(
            source_file,
            raw_rows_by_file[source_file],
            config,
            validator=BASE_VALIDATORS.get(source_file),
        )
        clean_rows_by_file[source_file] = rows
        file_stats[source_file]["duplicates_removed"] += duplicates_removed
        add_rejections(source_file, source_rejections, file_stats, rejection_counts, rejected_rows)

    return clean_rows_by_file


def apply_cross_file_validations(clean_rows_by_file, file_stats, rejected_rows, rejection_counts):
    category_names = {row["name"] for row in clean_rows_by_file["categories.csv"]}
    clean_products, product_category_rejections = validate_product_categories(
        "products.csv",
        clean_rows_by_file["products.csv"],
        category_names,
    )
    clean_rows_by_file["products.csv"] = clean_products
    add_rejections(
        "products.csv",
        product_category_rejections,
        file_stats,
        rejection_counts,
        rejected_rows,
    )

    clean_inventory, inventory_product_rejections = reject_conflicting_inventory_products(
        "inventory.csv",
        clean_rows_by_file["inventory.csv"],
    )
    clean_rows_by_file["inventory.csv"] = clean_inventory
    add_rejections(
        "inventory.csv",
        inventory_product_rejections,
        file_stats,
        rejection_counts,
        rejected_rows,
    )

    customer_ids = {row["id"] for row in clean_rows_by_file["customers.csv"]}
    product_ids = {row["id"] for row in clean_rows_by_file["products.csv"]}
    clean_sales, sales_fk_rejections, clean_inventory, inventory_fk_rejections = (
        validate_foreign_keys(
            clean_rows_by_file["sales.csv"],
            clean_rows_by_file["inventory.csv"],
            customer_ids,
            product_ids,
        )
    )

    clean_rows_by_file["sales.csv"] = clean_sales
    clean_rows_by_file["inventory.csv"] = clean_inventory

    add_rejections("sales.csv", sales_fk_rejections, file_stats, rejection_counts, rejected_rows)
    add_rejections(
        "inventory.csv",
        inventory_fk_rejections,
        file_stats,
        rejection_counts,
        rejected_rows,
    )


def write_outputs(clean_rows_by_file, file_stats, rejected_rows, rejection_counts):
    for source_file, config in FILE_CONFIG.items():
        clean_rows = clean_rows_by_file[source_file]
        file_stats[source_file]["rows_clean"] = len(clean_rows)
        write_csv_file(PROCESSED_DIR / config["clean_name"], config["fields"], clean_rows)

    write_csv_file(PROCESSED_DIR / "rejected_rows.csv", REJECTED_ROW_FIELDS, rejected_rows)
    write_json_file(
        PROCESSED_DIR / "data_quality_report.json",
        build_data_quality_report(file_stats, rejection_counts),
    )
    write_json_file(PROCESSED_DIR / "metrics.json", build_metrics(clean_rows_by_file))


def main():
    ensure_output_directory()

    rejected_rows = []
    rejection_counts = defaultdict(int)
    raw_rows_by_file, file_stats = load_raw_rows()
    clean_rows_by_file = process_base_files(
        raw_rows_by_file,
        file_stats,
        rejected_rows,
        rejection_counts,
    )

    apply_cross_file_validations(
        clean_rows_by_file,
        file_stats,
        rejected_rows,
        rejection_counts,
    )
    write_outputs(clean_rows_by_file, file_stats, rejected_rows, rejection_counts)

    print(f"Processed files written to: {PROCESSED_DIR}")


if __name__ == "__main__":
    main()
