import csv
import random
from datetime import date, timedelta
from pathlib import Path

from faker import Faker


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
OUTPUT_DIR = PROJECT_ROOT / "data" / "raw"

fake = Faker("en_US")

random.seed(42)
Faker.seed(42)

CUSTOMER_COUNT = 200
PRODUCT_COUNT = 60
SALE_COUNT = 2500

REGIONS = ["North", "South", "East", "West", "Central"]

CATEGORIES = [
    "Electronics",
    "Clothing",
    "Home",
    "Grocery",
    "Sports",
]

SUPPLIERS = [
    "Nova Supply",
    "Urban Trade",
    "Blue Market",
    "Prime Source",
    "Core Retail",
    "Vertex Goods",
    "Sun Distribution",
]

PRICE_BY_CATEGORY = {
    "Electronics": (150, 3500),
    "Clothing": (20, 300),
    "Home": (40, 1200),
    "Grocery": (5, 80),
    "Sports": (30, 900),
}

LOW_STOCK_PRODUCT_IDS = [1, 2, 3]
LOW_STOCK_TARGETS = {1: 12, 2: 18, 3: 24}
CHURN_CUSTOMER_IDS = [1, 2, 3, 4, 5, 6]
ACTIVE_CUSTOMER_IDS = [20, 21, 22, 23, 24, 25]
INVENTORY_CONFLICT_PRODUCT_ID = 14
INVALID_STOCK_PRODUCT_ID = 15


def get_price(category):
    min_price, max_price = PRICE_BY_CATEGORY[category]
    return round(random.uniform(min_price, max_price), 2)


def calculate_turnover_rate(sold_quantity, current_stock):
    if current_stock <= 0:
        return 0

    return round(sold_quantity / current_stock, 2)


def save_csv(filename, fieldnames, rows):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_DIR / filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def get_next_id(rows):
    return max(row["id"] for row in rows) + 1


def append_sale(sales, customer_id, product_id, sale_date, quantity):
    sales.append(
        {
            "id": get_next_id(sales),
            "customer_id": customer_id,
            "product_id": product_id,
            "date": sale_date,
            "quantity": quantity,
        }
    )


def build_sales_totals(products, sales):
    totals = {product["id"]: 0 for product in products}

    for sale in sales:
        totals[sale["product_id"]] = totals.get(sale["product_id"], 0) + sale["quantity"]

    return totals


def find_inventory_row(inventory, product_id):
    for row in inventory:
        if row["product_id"] == product_id:
            return row

    return None


def recalculate_inventory_turnover(inventory, products, sales):
    sales_totals = build_sales_totals(products, sales)

    for row in inventory:
        sold_quantity = sales_totals.get(row["product_id"], 0)
        current_stock = row["current_stock"]
        row["turnover_rate"] = calculate_turnover_rate(sold_quantity, current_stock)


def generate_customers():
    customers = []

    for i in range(1, CUSTOMER_COUNT + 1):
        customer = {
            "id": i,
            "name": fake.name(),
            "age": random.randint(18, 75),
            "region": random.choice(REGIONS),
        }
        customers.append(customer)

    return customers


def generate_products():
    products = []

    for i in range(1, PRODUCT_COUNT + 1):
        category = random.choice(CATEGORIES)

        product = {
            "id": i,
            "category": category,
            "price": get_price(category),
            "supplier": random.choice(SUPPLIERS),
        }
        products.append(product)

    return products


def generate_sales(customers, products):
    sales = []

    customer_ids = [customer["id"] for customer in customers]
    product_ids = [product["id"] for product in products]

    # To improve the analyses. Make it more realistic :)
    weighted_product_ids = product_ids + random.choices(product_ids, k=len(product_ids) * 3)

    for i in range(1, SALE_COUNT + 1):
        sale = {
            "id": i,
            "customer_id": random.choice(customer_ids),
            "product_id": random.choice(weighted_product_ids),
            "date": fake.date_between(start_date="-12M", end_date="today").isoformat(),
            "quantity": random.randint(1, 5),
        }
        sales.append(sale)

    return sales


def generate_categories():
    categories = []

    for i, category_name in enumerate(CATEGORIES, start=1):
        category = {
            "id": i,
            "name": category_name,
        }
        categories.append(category)

    return categories


def generate_inventory(products, sales):
    inventory = []
    sales_by_product = build_sales_totals(products, sales)

    for product in products:
        product_id = product["id"]
        sold_quantity = sales_by_product.get(product_id, 0)
        current_stock = random.randint(20, 300)

        inventory_item = {
            "id": product_id,
            "product_id": product_id,
            "current_stock": current_stock,
            "turnover_rate": calculate_turnover_rate(sold_quantity, current_stock),
        }
        inventory.append(inventory_item)

    return inventory


def inject_business_scenarios(customers, products, sales, inventory):
    recent_date = date.today().isoformat()
    old_date = (date.today() - timedelta(days=180)).isoformat()

    for sale in sales:
        if sale["customer_id"] in CHURN_CUSTOMER_IDS:
            sale["date"] = old_date

    for customer_id in CHURN_CUSTOMER_IDS:
        if not any(sale["customer_id"] == customer_id for sale in sales):
            append_sale(sales, customer_id, LOW_STOCK_PRODUCT_IDS[0], old_date, 1)

    for index, product_id in enumerate(LOW_STOCK_PRODUCT_IDS):
        for offset in range(30):
            customer_id = ACTIVE_CUSTOMER_IDS[(index + offset) % len(ACTIVE_CUSTOMER_IDS)]
            append_sale(sales, customer_id, product_id, recent_date, 5)

    sales_totals = build_sales_totals(products, sales)
    excluded_product_ids = set(LOW_STOCK_PRODUCT_IDS) | {
        INVENTORY_CONFLICT_PRODUCT_ID,
        INVALID_STOCK_PRODUCT_ID,
    }
    low_sales_products = [
        product_id
        for product_id, _ in sorted(sales_totals.items(), key=lambda item: (item[1], item[0]))
        if product_id not in excluded_product_ids
    ][:3]

    for product_id, stock in LOW_STOCK_TARGETS.items():
        inventory_row = find_inventory_row(inventory, product_id)
        if inventory_row:
            inventory_row["current_stock"] = stock

    for product_id, stock in zip(low_sales_products, [220, 240, 260]):
        inventory_row = find_inventory_row(inventory, product_id)
        if inventory_row:
            inventory_row["current_stock"] = stock

    recalculate_inventory_turnover(inventory, products, sales)


def inject_customer_issues(customers):
    customers[0]["region"] = ""

    customers.append(
        {
            "id": get_next_id(customers),
            "name": "",
            "age": 34,
            "region": "North",
        }
    )

    customers.append(dict(customers[1]))


def inject_product_issues(products):
    products[0]["supplier"] = ""

    products.append(
        {
            "id": get_next_id(products),
            "category": "Electronics",
            "price": 0,
            "supplier": "Nova Supply",
        }
    )

    conflict_id = get_next_id(products)
    products.append(
        {
            "id": conflict_id,
            "category": "Home",
            "price": 249.99,
            "supplier": "Blue Market",
        }
    )
    products.append(
        {
            "id": conflict_id,
            "category": "Sports",
            "price": 799.99,
            "supplier": "Prime Source",
        }
    )

    products.append(
        {
            "id": get_next_id(products),
            "category": "Toys",
            "price": 49.99,
            "supplier": "Urban Trade",
        }
    )


def inject_sales_issues(customers, products, sales):
    valid_customer_id = customers[9]["id"]
    valid_product_id = products[4]["id"]

    sales.append(
        {
            "id": get_next_id(sales),
            "customer_id": valid_customer_id,
            "product_id": valid_product_id,
            "date": date.today().isoformat(),
            "quantity": 0,
        }
    )
    sales.append(
        {
            "id": get_next_id(sales),
            "customer_id": get_next_id(customers) + 999,
            "product_id": valid_product_id,
            "date": date.today().isoformat(),
            "quantity": 2,
        }
    )
    sales.append(
        {
            "id": get_next_id(sales),
            "customer_id": valid_customer_id,
            "product_id": get_next_id(products) + 999,
            "date": date.today().isoformat(),
            "quantity": 2,
        }
    )
    sales.append(
        {
            "id": get_next_id(sales),
            "customer_id": valid_customer_id,
            "product_id": valid_product_id,
            "date": "03/15/2026",
            "quantity": 2,
        }
    )

    sales.append(dict(sales[0]))


def inject_inventory_issues(products, inventory):
    inventory.append(
        {
            "id": get_next_id(inventory),
            "product_id": INVALID_STOCK_PRODUCT_ID,
            "current_stock": -5,
            "turnover_rate": 0,
        }
    )
    inventory.append(
        {
            "id": get_next_id(inventory),
            "product_id": get_next_id(products) + 999,
            "current_stock": 40,
            "turnover_rate": 0,
        }
    )

    base_row = find_inventory_row(inventory, INVENTORY_CONFLICT_PRODUCT_ID)
    inventory.append(
        {
            "id": get_next_id(inventory),
            "product_id": INVENTORY_CONFLICT_PRODUCT_ID,
            "current_stock": base_row["current_stock"] + 45,
            "turnover_rate": round(base_row["turnover_rate"] + 0.5, 2),
        }
    )


def inject_category_issues(categories):
    categories.append(
        {
            "id": get_next_id(categories),
            "name": "",
        }
    )


def main():
    customers = generate_customers()
    products = generate_products()
    sales = generate_sales(customers, products)
    categories = generate_categories()
    inventory = generate_inventory(products, sales)

    inject_business_scenarios(customers, products, sales, inventory)
    inject_customer_issues(customers)
    inject_product_issues(products)
    inject_sales_issues(customers, products, sales)
    inject_inventory_issues(products, inventory)
    inject_category_issues(categories)

    save_csv(
        "customers.csv",
        ["id", "name", "age", "region"],
        customers,
    )

    save_csv(
        "products.csv",
        ["id", "category", "price", "supplier"],
        products,
    )

    save_csv(
        "sales.csv",
        ["id", "customer_id", "product_id", "date", "quantity"],
        sales,
    )

    save_csv(
        "categories.csv",
        ["id", "name"],
        categories,
    )

    save_csv(
        "inventory.csv",
        ["id", "product_id", "current_stock", "turnover_rate"],
        inventory,
    )

    print(f"- {OUTPUT_DIR / 'customers.csv'}")
    print(f"- {OUTPUT_DIR / 'products.csv'}")
    print(f"- {OUTPUT_DIR / 'sales.csv'}")
    print(f"- {OUTPUT_DIR / 'categories.csv'}")
    print(f"- {OUTPUT_DIR / 'inventory.csv'}")


if __name__ == "__main__":
    main()
