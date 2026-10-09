Branches 
branch_id | INT | PK | identifies the branch
name      | TEXT | - |
city      | TEXT | - |
address   | TEXT | - |

Suppliers
supplier_id | INT | PK | identifies the supplier
name      | TEXT | - |
contact_info      | TEXT | - |

Products
product_id | INT | PK | identifies the product
name      | TEXT | - |
category      | TEXT | - |
unit_price      | NUMERIC(10,2) | - |
supplier_id | INT | FK | → suppliers.supplier_id

Stock
stock_id | INT | PK | identifies the stock
quantity      | INT | - |
expiry_date      | DATE | - |
reorder_level      | INT | - |
batch_number | TEXT | - |
branch_id  | INT | FK | -> branches.branch_id
product_id  | INT | FK | → products.product_id
UNIQUE (branch_id, product_id, batch_number)

Sales
sale_id | INT | PK | identifies the sale 
sale_time | TIMESTAMP | - |
total      | NUMERIC(10,2) | - |
branch_id  | INT | FK | -> branches.branch_id


Sale_Items
sale_item_id | INT | PK | identifies the sale line
product_id | INT | FK |  → products.product_id
quantity      | INT | - |
unit_price      | NUMERIC(10,2) | - |
sale_id | INT | FK | -> sales.sale_id 

products.supplier_id → suppliers.supplier_id
stock.branch_id → branches.branch_id
stock.product_id -> products.product_id
sales.branch_id -> branches.branch_d
sale_items.product_id -> products.product_id
sale_items.sale_id -> sales.sale_id

2.) It's because one sale has many products. If you put all products in each sale, it would break normalization rules.

4.) No. Stock would need to have multiple rows. Each row would represent a batch and an extra column would be needed, e.g. batch number, to identify which batch the product is a part of. For each branch and product, there should be no duplicate batch number.

5.) I think products should store the unit price. Sale_items should store its own unit price as well because the price might change.