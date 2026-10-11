SELECT 
    b.name AS branch_name,
    p.name AS product_name,
    sup.name AS supplier_name,
    s.batch_number AS batch_number,
    s.quantity AS quantity,
    s.reorder_level AS reorder_level
FROM stock s
JOIN branches b 
    ON s.branch_id = b.branch_id
JOIN products p 
    ON s.product_id = p.product_id
JOIN suppliers sup 
    ON p.supplier_id = sup.supplier_id
WHERE s.quantity <= s.reorder_level
ORDER BY 
    branch_name,
    s.quantity ASC;


-- Report 2: Batches expired or expiring within 60 days that still have stock on hand
SELECT 
    b.name AS branch_name,
    p.name AS product_name,
    s.batch_number AS batch_number,
    s.quantity AS quantity,
    s.expiry_date AS expiry_date,
    (s.expiry_date - CURRENT_DATE) AS days_left,
    CASE 
        WHEN s.expiry_date < CURRENT_DATE THEN 'EXPIRED'
        ELSE 'EXPIRING SOON'
    END AS status
FROM stock s
JOIN branches b 
    ON s.branch_id = b.branch_id
JOIN products p 
    ON s.product_id = p.product_id
WHERE s.quantity > 0
  AND s.expiry_date <= CURRENT_DATE + 60
ORDER BY 
    s.expiry_date ASC;