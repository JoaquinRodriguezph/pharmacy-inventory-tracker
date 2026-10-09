Order of table creation:

branches, suppliers, products (needs suppliers), stock (needs branches and products), sales (needs branches), sale_items (needs sales and products)

Quantities:
4 branches, 8 suppliers, 60 products, 1-4 batches per product per branch, 700 sales over the last 12 months.

Low stock: how will some stock rows end up at or below reorder_level?
- most rows get a random quantity of 50 to 200, but about 15% get a quantity between 0 and their reorder_level. The reorder_level is 30 units. In reality, it also depends on how long the supplier gets to the branch.

Near expiry: how will some batches have expiry dates in the next 30 to 60 days (and a few already expired)?
- I believe each batch has just one expiry date and so the expiry date is just per batch. most batches expire 3 to 24 months from today, about 10% expire within the next 60 days, and about 3% are already expired.

Top sellers / monthly sales: how will sales be spread across different months and branches, so the monthly report has several rows?
- The monthly report would be an aggergate of the sum of the sales across those different months and branches. Maybe an aggregate per branch per month and then a total sum of them across the months. The script would make some products sell more than others, wherein popular products get larger weights. each sale gets 1 to 5 line items (random). every sale gets a random sale_time in the last 365 days.

Categories: list 5 to 6 product categories you’ll use (for example Pain Relief, Antibiotics, Vitamins).
- Prescription
- OTC Medicine
- Vitamins
- Surgical Supplies
- Personal Care
- Medical Devices

The tricky one. sales.total is stored in the sales table, but the real amounts live in sale_items. When the script creates a sale, how should total get its value so it matches the line items? Write your approach in one or two sentences. (Hint: you need to know the line items before you can insert the sale’s total, or update it afterward.)
- It picks the products and quantities for a sale, calculates the total, and inserts the sale with the total. Unit price is copied from product current price. Each sale picks its branch using slightly different weights so that the sales are not identical. branch weights  are 40/30/20/10.

Known simplification: seeded sales don’t reduce stock.quantity.