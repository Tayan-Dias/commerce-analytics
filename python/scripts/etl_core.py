from collections import defaultdict
from datetime import date, timedelta


FILE_CONFIG = {
    "customers.csv": {
        "clean_name": "clean_customers.csv",
        "fields": ["id", "name", "age", "region"],
        "critical_fields": ["id", "name", "age"],
        "defaults": {"region": "Unknown"},
        "id_field": "id",
    },
    "products.csv": {
        "clean_name": "clean_products.csv",
        "fields": ["id", "category", "price", "supplier"],
        "critical_fields": ["id", "category", "price"],
        "defaults": {"supplier": "Unknown"},
        "id_field": "id",
    },
    "sales.csv": {
        "clean_name": "clean_sales.csv",
        "fields": ["id", "customer_id", "product_id", "date", "quantity"],
        "critical_fields": ["id", "customer_id", "product_id", "date", "quantity"],
        "defaults": {},
        "id_field": "id",
    },
    "inventory.csv": {
        "clean_name": "clean_inventory.csv",
        "fields": ["id", "product_id", "current_stock", "turnover_rate"],
        "critical_fields": ["id", "product_id", "current_stock"],
        "defaults": {},
        "id_field": "id",
    },
    "categories.csv": {
        "clean_name": "clean_categories.csv",
        "fields": ["id", "name"],
        "critical_fields": ["id", "name"],
        "defaults": {},
        "id_field": "id",
    },
}

REJECTED_ROW_FIELDS = [
    "source_file",
    "rejection_reason",
    "id",
    "name",
    "age",
    "region",
    "category",
    "price",
    "supplier",
    "customer_id",
    "product_id",
    "date",
    "quantity",
    "current_stock",
    "turnover_rate",
]


def fill_non_critical_missing_values(rows, defaults):
    filled_rows = []

    for row in rows:
        updated_row = dict(row)

        for field, default_value in defaults.items():
            if not updated_row.get(field):
                updated_row[field] = default_value

        filled_rows.append(updated_row)

    return filled_rows


def reject_rows_with_missing_critical_fields(source_file, rows, critical_fields):
    valid_rows = []
    rejected_rows = []

    for row in rows:
        if any(not row.get(field) for field in critical_fields):
            rejected_rows.append(build_rejected_row(source_file, "missing_critical_field", row))
            continue

        valid_rows.append(row)

    return valid_rows, rejected_rows


def remove_exact_duplicates(rows, fieldnames):
    unique_rows = []
    seen_signatures = set()
    duplicates_removed = 0

    for row in rows:
        signature = row_signature(row, fieldnames)

        if signature in seen_signatures:
            duplicates_removed += 1
            continue

        seen_signatures.add(signature)
        unique_rows.append(row)

    return unique_rows, duplicates_removed


def reject_conflicting_duplicate_ids(source_file, rows, id_field, fieldnames):
    rows_by_id = defaultdict(list)
    valid_rows = []
    rejected_rows = []

    for row in rows:
        rows_by_id[row[id_field]].append(row)

    for row_group in rows_by_id.values():
        if len(row_group) == 1:
            valid_rows.append(row_group[0])
            continue

        signatures = {row_signature(row, fieldnames) for row in row_group}

        if len(signatures) == 1:
            valid_rows.append(row_group[0])
            continue

        for row in row_group:
            rejected_rows.append(build_rejected_row(source_file, "conflicting_duplicate_id", row))

    return valid_rows, rejected_rows


def validate_products(source_file, rows):
    valid_rows = []
    rejected_rows = []

    for row in rows:
        price = parse_float(row.get("price"))

        if price is None or price <= 0:
            rejected_rows.append(build_rejected_row(source_file, "invalid_price", row))
            continue

        valid_rows.append(row)

    return valid_rows, rejected_rows


def validate_sales(source_file, rows):
    valid_rows = []
    rejected_rows = []

    for row in rows:
        if parse_iso_date(row.get("date")) is None:
            rejected_rows.append(build_rejected_row(source_file, "invalid_date", row))
            continue

        quantity = parse_int(row.get("quantity"))

        if quantity is None or quantity <= 0:
            rejected_rows.append(build_rejected_row(source_file, "invalid_quantity", row))
            continue

        valid_rows.append(row)

    return valid_rows, rejected_rows


def validate_inventory(source_file, rows):
    valid_rows = []
    rejected_rows = []

    for row in rows:
        current_stock = parse_int(row.get("current_stock"))

        if current_stock is None or current_stock < 0:
            rejected_rows.append(build_rejected_row(source_file, "invalid_current_stock", row))
            continue

        valid_rows.append(row)

    return valid_rows, rejected_rows


def validate_product_categories(source_file, rows, category_names):
    valid_rows = []
    rejected_rows = []

    for row in rows:
        if row["category"] not in category_names:
            rejected_rows.append(build_rejected_row(source_file, "invalid_category", row))
            continue

        valid_rows.append(row)

    return valid_rows, rejected_rows


def reject_conflicting_inventory_products(source_file, rows):
    rows_by_product_id = defaultdict(list)
    valid_rows = []
    rejected_rows = []

    for row in rows:
        rows_by_product_id[row["product_id"]].append(row)

    for row_group in rows_by_product_id.values():
        if len(row_group) == 1:
            valid_rows.append(row_group[0])
            continue

        for row in row_group:
            rejected_rows.append(build_rejected_row(source_file, "conflicting_inventory_product", row))

    return valid_rows, rejected_rows


def validate_foreign_keys(sales_rows, inventory_rows, customer_ids, product_ids):
    valid_sales = []
    rejected_sales = []
    valid_inventory = []
    rejected_inventory = []

    for row in sales_rows:
        if row["customer_id"] not in customer_ids or row["product_id"] not in product_ids:
            rejected_sales.append(build_rejected_row("sales.csv", "invalid_foreign_key", row))
            continue

        valid_sales.append(row)

    for row in inventory_rows:
        if row["product_id"] not in product_ids:
            rejected_inventory.append(build_rejected_row("inventory.csv", "invalid_foreign_key", row))
            continue

        valid_inventory.append(row)

    return valid_sales, rejected_sales, valid_inventory, rejected_inventory


def compute_revenue_by_region(customers_rows, products_rows, sales_rows):
    customers_by_id = {row["id"]: row for row in customers_rows}
    products_by_id = {row["id"]: row for row in products_rows}
    revenue_by_region = defaultdict(float)

    for sale in sales_rows:
        customer = customers_by_id.get(sale["customer_id"])
        product = products_by_id.get(sale["product_id"])

        if not customer or not product:
            continue

        revenue_by_region[customer.get("region") or "Unknown"] += (
            (parse_int(sale["quantity"]) or 0) * (parse_float(product["price"]) or 0)
        )

    return {
        region: round(total_revenue, 2)
        for region, total_revenue in sorted(revenue_by_region.items())
    }


def compute_top_selling_products(products_rows, sales_rows):
    products_by_id = {row["id"]: row for row in products_rows}
    sold_quantity_by_product = build_sold_quantity_by_product(products_rows, sales_rows)
    ranking = []

    for product_id, total_quantity_sold in sold_quantity_by_product.items():
        if total_quantity_sold <= 0:
            continue

        product = products_by_id[product_id]
        ranking.append(
            {
                "product_id": format_id(product_id),
                "category": product["category"],
                "total_quantity_sold": total_quantity_sold,
            }
        )

    ranking.sort(key=lambda item: (-item["total_quantity_sold"], str(item["product_id"])))
    return ranking


def compute_customer_churn(customers_rows, sales_rows):
    total_customers = len(customers_rows)

    if not sales_rows:
        active_customers = 0
        churned_customers = total_customers
    else:
        max_sales_date = max(parse_iso_date(row["date"]) for row in sales_rows)
        cutoff_date = max_sales_date - timedelta(days=90)
        active_customer_ids = {
            row["customer_id"]
            for row in sales_rows
            if parse_iso_date(row["date"]) >= cutoff_date
        }
        active_customers = len(active_customer_ids)
        churned_customers = max(total_customers - active_customers, 0)

    return {
        "total_customers": total_customers,
        "active_customers": active_customers,
        "churned_customers": churned_customers,
        "churn_rate": round(churned_customers / total_customers, 4) if total_customers else 0,
    }


def compute_low_stock_high_sales(products_rows, inventory_rows, sales_rows):
    products_by_id = {row["id"]: row for row in products_rows}
    sold_quantity_by_product = build_sold_quantity_by_product(products_rows, sales_rows)
    average_sold_quantity = compute_average_sold_quantity(sold_quantity_by_product)
    rows = []

    for inventory_row in inventory_rows:
        product_id = inventory_row["product_id"]
        current_stock = parse_int(inventory_row["current_stock"]) or 0
        total_quantity_sold = sold_quantity_by_product.get(product_id, 0)

        if current_stock < 30 and total_quantity_sold > average_sold_quantity:
            rows.append(
                {
                    "product_id": format_id(product_id),
                    "category": products_by_id.get(product_id, {}).get("category", ""),
                    "current_stock": current_stock,
                    "total_quantity_sold": total_quantity_sold,
                }
            )

    rows.sort(key=lambda item: (item["current_stock"], -item["total_quantity_sold"]))
    return rows


def compute_overstock_low_sales(products_rows, inventory_rows, sales_rows):
    products_by_id = {row["id"]: row for row in products_rows}
    sold_quantity_by_product = build_sold_quantity_by_product(products_rows, sales_rows)
    average_sold_quantity = compute_average_sold_quantity(sold_quantity_by_product)
    rows = []

    for inventory_row in inventory_rows:
        product_id = inventory_row["product_id"]
        current_stock = parse_int(inventory_row["current_stock"]) or 0
        total_quantity_sold = sold_quantity_by_product.get(product_id, 0)

        if current_stock > 150 and total_quantity_sold < average_sold_quantity:
            rows.append(
                {
                    "product_id": format_id(product_id),
                    "category": products_by_id.get(product_id, {}).get("category", ""),
                    "current_stock": current_stock,
                    "total_quantity_sold": total_quantity_sold,
                }
            )

    rows.sort(key=lambda item: (-item["current_stock"], item["total_quantity_sold"]))
    return rows


def compute_turnover_by_category(products_rows, inventory_rows, sales_rows):
    sold_quantity_by_product = build_sold_quantity_by_product(products_rows, sales_rows)
    inventory_by_product = {row["product_id"]: row for row in inventory_rows}
    totals_by_category = defaultdict(lambda: {"total_quantity_sold": 0, "current_stock": 0})

    for product in products_rows:
        category = product["category"]
        product_id = product["id"]
        totals_by_category[category]["total_quantity_sold"] += sold_quantity_by_product.get(
            product_id, 0
        )
        totals_by_category[category]["current_stock"] += parse_int(
            inventory_by_product.get(product_id, {}).get("current_stock")
        ) or 0

    turnover_rows = []

    for category, totals in totals_by_category.items():
        current_stock = totals["current_stock"]
        turnover_rate = 0 if current_stock == 0 else round(
            totals["total_quantity_sold"] / current_stock, 4
        )

        turnover_rows.append(
            {
                "category": category,
                "total_quantity_sold": totals["total_quantity_sold"],
                "current_stock": current_stock,
                "turnover_rate": turnover_rate,
            }
        )

    turnover_rows.sort(key=lambda item: (-item["turnover_rate"], item["category"]))
    return turnover_rows


def build_data_quality_report(file_stats, rejection_counts_by_reason):
    return {
        "files": file_stats,
        "rejection_counts_by_reason": dict(sorted(rejection_counts_by_reason.items())),
    }


def build_rejected_row(source_file, rejection_reason, row):
    rejected_row = {field: "" for field in REJECTED_ROW_FIELDS}
    rejected_row["source_file"] = source_file
    rejected_row["rejection_reason"] = rejection_reason

    for field, value in row.items():
        if field in rejected_row:
            rejected_row[field] = value

    return rejected_row


def add_rejections(source_file, new_rejections, file_stats, rejection_counts, all_rejections):
    if not new_rejections:
        return

    file_stats[source_file]["rows_rejected"] += len(new_rejections)
    all_rejections.extend(new_rejections)

    for row in new_rejections:
        rejection_counts[row["rejection_reason"]] += 1


def row_signature(row, fieldnames):
    return tuple(row.get(field, "") for field in fieldnames)


def parse_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def parse_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def parse_iso_date(value):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def format_id(value):
    parsed_value = parse_int(value)
    return parsed_value if parsed_value is not None else value


def build_sold_quantity_by_product(products_rows, sales_rows):
    sold_quantity_by_product = {row["id"]: 0 for row in products_rows}

    for sale in sales_rows:
        sold_quantity_by_product[sale["product_id"]] = sold_quantity_by_product.get(
            sale["product_id"], 0
        ) + (parse_int(sale["quantity"]) or 0)

    return sold_quantity_by_product


def compute_average_sold_quantity(sold_quantity_by_product):
    if not sold_quantity_by_product:
        return 0

    return sum(sold_quantity_by_product.values()) / len(sold_quantity_by_product)


def process_source_rows(source_file, rows, config, validator=None):
    rejections = []

    rows = fill_non_critical_missing_values(rows, config["defaults"])
    rows, missing_rejections = reject_rows_with_missing_critical_fields(
        source_file,
        rows,
        config["critical_fields"],
    )
    rows, duplicates_removed = remove_exact_duplicates(rows, config["fields"])
    rows, duplicate_rejections = reject_conflicting_duplicate_ids(
        source_file,
        rows,
        config["id_field"],
        config["fields"],
    )

    rejections.extend(missing_rejections)
    rejections.extend(duplicate_rejections)

    if validator is not None:
        rows, validation_rejections = validator(source_file, rows)
        rejections.extend(validation_rejections)

    return rows, rejections, duplicates_removed


def build_metrics(clean_rows_by_file):
    return {
        "revenue_by_region": compute_revenue_by_region(
            clean_rows_by_file["customers.csv"],
            clean_rows_by_file["products.csv"],
            clean_rows_by_file["sales.csv"],
        ),
        "top_selling_products": compute_top_selling_products(
            clean_rows_by_file["products.csv"],
            clean_rows_by_file["sales.csv"],
        ),
        "customer_churn": compute_customer_churn(
            clean_rows_by_file["customers.csv"],
            clean_rows_by_file["sales.csv"],
        ),
        "low_stock_high_sales": compute_low_stock_high_sales(
            clean_rows_by_file["products.csv"],
            clean_rows_by_file["inventory.csv"],
            clean_rows_by_file["sales.csv"],
        ),
        "overstock_low_sales": compute_overstock_low_sales(
            clean_rows_by_file["products.csv"],
            clean_rows_by_file["inventory.csv"],
            clean_rows_by_file["sales.csv"],
        ),
        "turnover_by_category": compute_turnover_by_category(
            clean_rows_by_file["products.csv"],
            clean_rows_by_file["inventory.csv"],
            clean_rows_by_file["sales.csv"],
        ),
    }
