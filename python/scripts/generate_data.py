import csv
import random
from pathlib import Path
from faker import Faker


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR if (SCRIPT_DIR / "data").exists() else SCRIPT_DIR.parent
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


def get_price(category):
    min_price, max_price = PRICE_BY_CATEGORY[category]
    return round(random.uniform(min_price, max_price), 2)


def save_csv(filename, fieldnames, rows):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_DIR / filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


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

    sales_by_product = {}

    for sale in sales:
        product_id = sale["product_id"]
        quantity = sale["quantity"]

        if product_id not in sales_by_product:
            sales_by_product[product_id] = 0

        sales_by_product[product_id] += quantity

    for product in products:
        product_id = product["id"]
        sold_quantity = sales_by_product.get(product_id, 0)

        current_stock = random.randint(20, 300)

        if sold_quantity == 0:
            turnover_rate = 0
        else:
            turnover_rate = round(sold_quantity / current_stock, 2)

        inventory_item = {
            "id": product_id,
            "product_id": product_id,
            "current_stock": current_stock,
            "turnover_rate": turnover_rate,
        }
        inventory.append(inventory_item)

    return inventory


def main():
    customers = generate_customers()
    products = generate_products()
    sales = generate_sales(customers, products)

    categories = generate_categories()
    inventory = generate_inventory(products, sales)

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
