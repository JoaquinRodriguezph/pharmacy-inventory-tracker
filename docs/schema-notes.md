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
quantity      | INT | - | default 0
expiry_date      | DATE | - | 
reorder_level      | INT | - | default 0
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
sales.branch_id -> branches.branch_id
sale_items.product_id -> products.product_id
sale_items.sale_id -> sales.sale_id
