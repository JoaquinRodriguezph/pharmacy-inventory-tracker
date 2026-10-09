from datetime import date, timedelta
import random
from faker import Faker
from db import get_connection

random.seed(42)
fake = Faker("en_PH")


def seed_branches(cur):
    branches = [
        ("Manila Main Branch", "Manila", "1004 Taft Avenue, Ermita"),
        ("Quezon City Hub", "Quezon City", "25 Diliman Commercial Center, Commonwealth Ave"),
        ("Calamba Crossing Branch", "Calamba", "Bgy. Real, National Highway"),
        ("Lucena City Center", "Lucena", "45 Quezon Avenue, Lucena City"),
    ]

    cur.executemany(
        "INSERT INTO branches (name, city, address) VALUES (%s, %s, %s)",
        branches,
    )


def seed_suppliers(cur):
    supplier_names = [
        "Luzon Pharma Corp.",
        "Drug Distribution Network",
        "Metro Med Inc.",
        "Therapharma Logistics",
        "Medreich Pharma Distributors",
        "BioCare Lifesciences Inc.",
        "Apotheca Integrative Logistics",
        "Dynasty Pharmaceuticals Depot",
    ]
    suppliers = [
        (name, fake.mobile_number())
        for name in supplier_names
    ]

    cur.executemany(
        "INSERT INTO suppliers (name, contact_info) VALUES (%s, %s)",
        suppliers,
    )


def seed_products(cur):
    cur.execute("SELECT supplier_id FROM suppliers")
    supplier_ids = [row[0] for row in cur.fetchall()]

    catalog = {
        "Prescription": {
            "price_range": (15.00, 120.00),
            "items": [
                "Amoxicillin 500mg Capsule",
                "Losartan 50mg Tablet",
                "Metformin 500mg Tablet",
                "Amlodipine 10mg Tablet",
                "Atorvastatin 20mg Tablet",
                "Azithromycin 500mg Tablet",
                "Cefalexin 500mg Capsule",
                "Ciprofloxacin 500mg Tablet",
                "Omeprazole 20mg Capsule",
                "Salbutamol 2mg Tablet",
            ],
        },
        "OTC Medicine": {
            "price_range": (3.50, 25.00),
            "items": [
                "Paracetamol 500mg Tablet",
                "Ibuprofen 200mg Softgel",
                "Loperamide 2mg Capsule",
                "Cetirizine 10mg Tablet",
                "Mefenamic Acid 500mg Capsule",
                "Antacid Chewable Tablet",
                "Dextromethorphan Syrup 60ml",
                "Phenylephrine HCl Decongestant 10mg",
                "Loratadine 10mg Tablet",
                "Oral Rehydration Salts 20g Sachet",
            ],
        },
        "Vitamins": {
            "price_range": (5.00, 45.00),
            "items": [
                "Ascorbic Acid (Vitamin C) 500mg",
                "Vitamin B-Complex Tablet",
                "Vitamin E 400IU Softgel",
                "Calcium + Vitamin D3 Tablet",
                "Zinc Sulfate 50mg Capsule",
                "Multivitamins + Iron Capsule",
                "Fish Oil Omega-3 1000mg Softgel",
                "Folic Acid 5mg Tablet",
                "Vitamin D3 1000IU Capsule",
                "Iron + Folic Acid Capsule",
            ],
        },
        "Surgical Supplies": {
            "price_range": (15.00, 350.00),
            "items": [
                "Sterile Gauze Pad 4x4 (Pack of 5)",
                "Medical Adhesive Tape 1-inch",
                "Latex Surgical Gloves (Size M)",
                "Surgical Disposable Face Mask (50s)",
                "Elastic Crepe Bandage 4-inch",
                "Disposable Syringe 3ml with Needle",
                "Alcohol Prep Pads (Box of 100)",
                "Povidone Iodine 10% Solution 60ml",
                "Sterile Cotton Balls (100s)",
                "Surgical Blade #11 (Box of 10)",
            ],
        },
        "Personal Care": {
            "price_range": (20.00, 180.00),
            "items": [
                "Isopropyl Alcohol 70% 500ml",
                "Antibacterial Hand Soap 250ml",
                "Hypoallergenic Baby Wipes (80s)",
                "Medicated Anti-Dandruff Shampoo 100ml",
                "Petroleum Jelly 100g Jar",
                "Sunscreen Gel SPF50 50ml",
                "Antiseptic Mouthwash 250ml",
                "Saline Nasal Spray 50ml",
                "Mosquito Repellent Lotion 100ml",
                "Hand Sanitizer Gel 100ml",
            ],
        },
        "Medical Devices": {
            "price_range": (500.00, 3200.00),
            "items": [
                "Digital Upper Arm Blood Pressure Monitor",
                "Fingertip Pulse Oximeter",
                "Infrared Forehead Thermometer",
                "Digital Blood Glucose Monitoring Kit",
                "Compressor Air Nebulizer Machine",
                "Automatic Blood Pressure Wrist Monitor",
                "Digital Body Weight Scale",
                "Standard Wheelchair 18-inch",
                "Adjustable Aluminum Walking Cane",
                "Hearing Aid Amplifier Rechargeable",
            ],
        },
    }

    products = []
    for category, meta in catalog.items():
        low, high = meta["price_range"]
        for name in meta["items"]:
            unit_price = round(random.uniform(low, high), 2)
            supplier_id = random.choice(supplier_ids)
            products.append((name, category, unit_price, supplier_id))

    cur.executemany(
        """
        INSERT INTO products (name, category, unit_price, supplier_id)
        VALUES (%s, %s, %s, %s)
        """,
        products,
    )


def seed_stock(cur):
    cur.execute("SELECT branch_id FROM branches")
    branch_ids = [row[0] for row in cur.fetchall()]

    cur.execute("SELECT product_id FROM products")
    product_ids = [row[0] for row in cur.fetchall()]

    today = date.today()
    stock_entries = []

    for branch_id in branch_ids:
        for product_id in product_ids:
            num_batches = random.randint(1, 4)
            for n in range(1, num_batches + 1):
                batch_number = f"B{product_id:03d}-{n}"
                reorder_level = 30

                # 15% low stock (0 to 30), 85% normal stock (50 to 200)
                if random.random() < 0.15:
                    quantity = random.randint(0, 30)
                else:
                    quantity = random.randint(50, 200)

                # ~3% expired, ~10% near expiry (30-60 days), ~87% standard (90-730 days)
                p = random.random()
                if p < 0.03:
                    days_delta = random.randint(-60, -1)
                elif p < 0.13:
                    days_delta = random.randint(30, 60)
                else:
                    days_delta = random.randint(90, 730)

                expiry_date = today + timedelta(days=days_delta)

                stock_entries.append((
                    branch_id,
                    product_id,
                    batch_number,
                    quantity,
                    expiry_date,
                    reorder_level,
                ))

    cur.executemany(
        """
        INSERT INTO stock (branch_id, product_id, batch_number, quantity, expiry_date, reorder_level)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        stock_entries,
    )


def main():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "TRUNCATE branches, suppliers, products, stock, sales, sale_items RESTART IDENTITY CASCADE;"
            )
            seed_branches(cur)
            seed_suppliers(cur)
            seed_products(cur)
            seed_stock(cur)


if __name__ == "__main__":
    main()