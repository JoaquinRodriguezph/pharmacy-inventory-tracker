from fastapi import FastAPI
from app.db import get_dict_connection

app = FastAPI(title="Pharmacy Inventory API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/branches")
def get_branches():
    with get_dict_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT branch_id, name, city, address FROM branches ORDER BY branch_id"
            )
            return cur.fetchall()


@app.get("/reports/low-stock")
def get_low_stock(branch_id: int | None = None):
    # Appended branch_id to the view so we can filter on the indexed integer primary key directly, avoiding string matching on branch_name.
    query = """
        SELECT branch_name, product_name, supplier_name, batch_number, quantity, reorder_level
        FROM v_low_stock
    """
    params = ()

    if branch_id is not None:
        query += " WHERE branch_id = %s"
        params = (branch_id,)

    query += " ORDER BY branch_name, quantity"

    with get_dict_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()


@app.get("/reports/monthly-sales")
def get_monthly_sales(branch_name: str | None = None):
    query = """
        SELECT branch_name, month, sales_count, total_revenue, avg_sale_value
        FROM v_monthly_sales
    """
    params = ()

    if branch_name is not None:
        query += " WHERE branch_name = %s"
        params = (branch_name,)

    query += " ORDER BY branch_name, month"

    with get_dict_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()


@app.get("/reports/expiring")
def get_expiring_batches(branch_id: int, days: int = 60):
    query = "SELECT * FROM fn_expiring_batches(%s, %s)"
    params = (branch_id, days)

    with get_dict_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()


@app.get("/reports/top-sellers")
def get_top_sellers(branch_name: str | None = None):
    query = """
        SELECT branch_name, product_name, units_sold, revenue, rank_in_branch
        FROM v_top_sellers
    """
    params = ()

    if branch_name is not None:
        query += " WHERE branch_name = %s"
        params = (branch_name,)

    query += " ORDER BY branch_name, rank_in_branch"

    with get_dict_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()


@app.get("/reports/restock")
def get_restock(branch_id: int):
    query = "SELECT * FROM fn_restock_list(%s)"
    params = (branch_id,)

    with get_dict_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()