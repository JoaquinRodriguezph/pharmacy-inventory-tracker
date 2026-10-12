-- View 1: Active batches that have reached or fallen below their reorder threshold
CREATE OR REPLACE VIEW v_low_stock AS
SELECT 
    b.name AS branch_name,
    p.name AS product_name,
    sup.name AS supplier_name,
    s.batch_number AS batch_number,
    s.quantity AS quantity,
    s.reorder_level AS reorder_level,
    s.branch_id AS branch_id
FROM stock s
JOIN branches b 
    ON s.branch_id = b.branch_id
JOIN products p 
    ON s.product_id = p.product_id
JOIN suppliers sup 
    ON p.supplier_id = sup.supplier_id
WHERE s.quantity <= s.reorder_level;

-- View 2: Aggregated monthly sales metrics by branch including count, revenue, and average value
CREATE OR REPLACE VIEW v_monthly_sales AS
SELECT 
    b.name AS branch_name,
    DATE_TRUNC('month', s.sale_time)::date AS month,
    COUNT(s.sale_id) AS sales_count,
    SUM(s.total) AS total_revenue,
    ROUND(AVG(s.total), 2) AS avg_sale_value
FROM sales s
JOIN branches b 
    ON s.branch_id = b.branch_id
GROUP BY 
    b.branch_id,
    DATE_TRUNC('month', s.sale_time)::date;

-- View 3: Top 5 best-selling products per branch based on units sold and revenue
CREATE OR REPLACE VIEW v_top_sellers AS
WITH totals AS (
    SELECT 
        b.branch_id,
        b.name AS branch_name,
        p.name AS product_name,
        SUM(si.quantity) AS units_sold,
        SUM(si.quantity * si.unit_price) AS revenue
    FROM sale_items si
    JOIN sales s 
        ON si.sale_id = s.sale_id
    JOIN branches b 
        ON s.branch_id = b.branch_id
    JOIN products p 
        ON si.product_id = p.product_id
    GROUP BY 
        b.branch_id,
        p.product_id
),
ranked AS (
    SELECT 
        branch_id,
        branch_name,
        product_name,
        units_sold,
        revenue,
        ROW_NUMBER() OVER (
            PARTITION BY branch_id 
            ORDER BY units_sold DESC, revenue DESC
        ) AS rank_in_branch
    FROM totals
)
SELECT 
    branch_name,
    product_name,
    units_sold,
    revenue,
    rank_in_branch
FROM ranked
WHERE rank_in_branch <= 5;