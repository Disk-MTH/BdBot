-- List category names
SELECT category_name
FROM category;

-- List all the products of the category 'drink' with a join and his price with a join
SELECT product_id, product_name, product_stock, product_picture, buy_price, sell_price
FROM product
         JOIN category ON product.category_id = category.category_id
         JOIN price ON product.price_id = price.price_id
WHERE category_name = 'drink';