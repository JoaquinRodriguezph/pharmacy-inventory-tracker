# pharmacy-inventory-tracker

## Overview & Tooling Disclosure
This project was developed with the assistance of AI tools (including LLM-based coding assistants) to aid in data schema design[cite: 1], mock data generation workflows[cite: 2], query optimization, and boilerplate FastAPI endpoint implementation. All generated database structures, queries, and application code have been independently verified, tested, and reviewed for schema accuracy, constraint integrity, and query performance[cite: 1].

---

## Database Rebuild Guide

To set up or completely rebuild the database from scratch, execute the scripts in the following order:

1. **`sql/01_schema.sql`**  
   Drops existing tables and constraints, then rebuilds the base tables and indexes[cite: 1].
2. **`python app/seed.py`** (or `python app\seed.py` on Windows)  
   Truncates table records and populates initial data for branches, suppliers, products, stock, and sales[cite: 2].
3. **`sql/03_views.sql`**  
   Creates standard views (`v_low_stock`, `v_monthly_sales`, and `v_top_sellers`).
4. **`sql/04_functions.sql`**  
   Defines stored analytical functions (`fn_restock_list` and `fn_expiring_batches`).

> **Gotcha / Rebuild Note:**  
> Running `01_schema.sql` uses `DROP TABLE ... CASCADE`[cite: 1], which automatically cascades and drops any dependent database views. The `TRUNCATE` command in `seed.py` does not affect views or functions, but any complete schema reset via `01_schema.sql` will remove them[cite: 1]. Always re-run `03_views.sql` and `04_functions.sql` following a schema rebuild.