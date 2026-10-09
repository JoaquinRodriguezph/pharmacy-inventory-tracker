   DROP TABLE IF EXISTS sale_items, sales, stock, products, suppliers, branches CASCADE;

   CREATE TABLE branches (
    branch_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT ,
    address TEXT 
   );

   CREATE TABLE suppliers (
    supplier_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    contact_info TEXT
   );

   CREATE TABLE products (
    product_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0),
    supplier_id INT NOT NULL,
    CONSTRAINT fk_products_supplier 
        FOREIGN KEY (supplier_id) 
        REFERENCES suppliers(supplier_id) 
        ON UPDATE CASCADE
        ON DELETE RESTRICT
   );

   CREATE TABLE stock (
    stock_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    branch_id INT NOT NULL,
    product_id INT NOT NULL,
    batch_number TEXT NOT NULL,
    quantity INT NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    expiry_date DATE NOT NULL,
    reorder_level INT DEFAULT 0 CHECK (reorder_level >= 0),
    CONSTRAINT uq_stock_branch_product_batch 
    UNIQUE (branch_id, product_id, batch_number),
    CONSTRAINT fk_stock_branch 
        FOREIGN KEY (branch_id) 
        REFERENCES branches(branch_id) 
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_stock_product
        FOREIGN KEY (product_id) 
        REFERENCES products(product_id) 
        ON UPDATE CASCADE
        ON DELETE RESTRICT
   );

   CREATE TABLE sales (
    sale_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    sale_time TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    total NUMERIC(10, 2) NOT NULL DEFAULT 0.00 CHECK (total >= 0),
    branch_id INT NOT NULL,
    CONSTRAINT fk_sales_branch 
        FOREIGN KEY (branch_id) 
        REFERENCES branches(branch_id) 
        ON UPDATE CASCADE
        ON DELETE RESTRICT
   );

    CREATE TABLE sale_items (
     sale_item_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
     sale_id INT NOT NULL,
     product_id INT NOT NULL,
     quantity INT NOT NULL CHECK (quantity > 0),
     unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0),
     CONSTRAINT fk_sale_items_sale 
          FOREIGN KEY (sale_id) 
          REFERENCES sales(sale_id) 
          ON UPDATE CASCADE
          ON DELETE CASCADE,
     CONSTRAINT fk_sale_items_product 
          FOREIGN KEY (product_id) 
          REFERENCES products(product_id) 
          ON UPDATE CASCADE
          ON DELETE RESTRICT
    );

CREATE INDEX idx_products_supplier_id ON products (supplier_id);
CREATE INDEX idx_stock_product_id ON stock (product_id);
CREATE INDEX idx_sales_branch_id ON sales (branch_id);
CREATE INDEX idx_sales_sale_time ON sales (sale_time);
CREATE INDEX idx_sale_items_sale_id ON sale_items (sale_id);
CREATE INDEX idx_sale_items_product_id ON sale_items (product_id);