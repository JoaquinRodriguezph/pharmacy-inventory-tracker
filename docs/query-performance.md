# Query Performance Analysis

We evaluated query execution plans on `sales` (filtering recent dates with and without an index) and `stock` (filtering by product and branch) using `EXPLAIN ANALYZE`.

### 1. Recent Sales Query (Indexed)
For `sale_time >= (CURRENT_DATE - 30)`, the planner selected a **Bitmap Index Scan** on `idx_sales_sale_time` followed by a **Bitmap Heap Scan**. The estimated total cost was **11.74** with an execution time of **0.092 ms** across 57 matched rows. The planner preferred this access path because navigating the index pages yielded a lower estimated cost than reading the entire relation sequentially.

### 2. Recent Sales Query (Sequential Scan)
After dropping `idx_sales_sale_time`, the same query defaulted to a **Seq Scan**, where the planner's estimated cost rose from **11.74 to 18.25** and execution took **0.103 ms** while filtering out 643 rows. While the index technically ran faster, a difference of ~0.01 ms on a single run is noise at this tiny scale; because the seeded dataset has only 700 rows, scanning the entire table is trivially cheap. The performance divergence between index traversals and sequential scans will expand substantially as the table scales into tens or hundreds of thousands of rows.

The dropped index was restored and confirmed present via:
```sql
SELECT indexname FROM pg_indexes WHERE tablename = 'sales';
```
```text
       indexname        
------------------------
 sales_pkey
 idx_sales_branch_id
 idx_sales_sale_time
(3 rows)
```

### 3. Stock Two-Column Filter
For `product_id = 5 AND branch_id = 2`, the planner performed a **Bitmap Index Scan** solely on `idx_stock_product_id`, retrieving 10 candidate rows and filtering out 9 in memory via `Filter: (branch_id = 2)` to leave 1 matching record (cost **9.38**, execution time **0.098 ms**). The existing constraint `UNIQUE (branch_id, product_id, batch_number)` can still be used, but less efficiently because `branch_id` is the leading column, leading the planner to favor the single-column index instead. A composite index on `(product_id, branch_id)` would allow the engine to evaluate both conditions directly within the index scan rather than filtering heap rows after the fact.