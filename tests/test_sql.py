import psycopg
import pytest
from app.db import get_dict_connection


@pytest.fixture
def cur():
    """Give each test a cursor, and roll back anything it changed."""
    conn = get_dict_connection()
    try:
        with conn.cursor() as cursor:
            yield cursor
    finally:
        conn.rollback()
        conn.close()


def test_sales_totals_match_line_items(cur):
    query = """
        SELECT COUNT(*) AS count
        FROM (
            SELECT 
                s.sale_id,
                s.total,
                SUM(si.quantity * si.unit_price) AS calculated_total
            FROM sales s
            JOIN sale_items si ON s.sale_id = si.sale_id
            GROUP BY s.sale_id, s.total
            HAVING s.total != SUM(si.quantity * si.unit_price)
        ) AS mismatches;
    """
    cur.execute(query)
    result = cur.fetchone()
    assert result["count"] == 0


def test_restock_list_only_includes_products_below_reorder_level(cur):
    cur.execute("SELECT * FROM fn_restock_list(%s)", (2,))
    rows = cur.fetchall()
    assert len(rows) > 0
    for row in rows:
        assert row["current_qty"] < row["reorder_level"]
        assert row["suggested_order_qty"] == row["reorder_level"] * 3 - row["current_qty"]


def test_expiring_batches_respects_day_window(cur):
    cur.execute("SELECT * FROM fn_expiring_batches(%s, %s)", (1, 30))
    rows = cur.fetchall()
    assert len(rows) > 0
    for row in rows:
        assert 0 <= row["days_left"] <= 30
        assert row["quantity"] > 0


def test_check_constraint_rejects_negative_stock(cur):
    with pytest.raises(psycopg.errors.CheckViolation):
        cur.execute(
            """
            INSERT INTO stock (
                branch_id, 
                product_id, 
                batch_number, 
                quantity, 
                reorder_level, 
                expiry_date
            )
            VALUES (%s, %s, %s, %s, %s, CURRENT_DATE + 90);
            """,
            (1, 1, "TEST-NEG", -1, 20),
        )