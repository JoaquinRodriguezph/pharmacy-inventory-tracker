-- Function 1: Generate suggested restock quantities for non-expired products below threshold
CREATE OR REPLACE FUNCTION fn_restock_list(p_branch_id INT)
RETURNS TABLE (
    product_name TEXT,
    supplier_name TEXT,
    current_qty BIGINT,
    reorder_level INT,
    suggested_order_qty BIGINT
)
LANGUAGE sql
AS $$
    SELECT 
        p.name AS product_name,
        sup.name AS supplier_name,
        SUM(s.quantity) AS current_qty,
        MAX(s.reorder_level) AS reorder_level,
        (MAX(s.reorder_level) * 3 - SUM(s.quantity))::BIGINT AS suggested_order_qty
    FROM stock s
    JOIN products p 
        ON s.product_id = p.product_id
    JOIN suppliers sup 
        ON p.supplier_id = sup.supplier_id
    WHERE s.branch_id = p_branch_id
      AND s.expiry_date >= CURRENT_DATE
    GROUP BY 
        p.product_id,
        p.name,
        sup.name
    HAVING SUM(s.quantity) < MAX(s.reorder_level)
    ORDER BY suggested_order_qty DESC;
$$;


-- Function 2: List active batches expiring within the specified number of days
CREATE OR REPLACE FUNCTION fn_expiring_batches(p_branch_id INT, p_days INT)
RETURNS TABLE (
    product_name TEXT,
    batch_number TEXT,
    quantity INT,
    expiry_date DATE,
    days_left INT
)
LANGUAGE sql
AS $$
    SELECT 
        p.name AS product_name,
        s.batch_number AS batch_number,
        s.quantity AS quantity,
        s.expiry_date AS expiry_date,
        (s.expiry_date - CURRENT_DATE)::INT AS days_left
    FROM stock s
    JOIN products p 
        ON s.product_id = p.product_id
    WHERE s.branch_id = p_branch_id
      AND s.quantity > 0
      AND s.expiry_date BETWEEN CURRENT_DATE AND (CURRENT_DATE + p_days)
    ORDER BY s.expiry_date ASC;
$$;