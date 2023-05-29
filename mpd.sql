CREATE TABLE IF NOT EXISTS category
(
    category_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name VARCHAR(1000) NOT NULL
);

CREATE TABLE IF NOT EXISTS price
(
    price_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    buy_price  DOUBLE NOT NULL,
    sell_price DOUBLE
);

CREATE TABLE IF NOT EXISTS product
(
    product_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name  VARCHAR(1000) NOT NULL,
    product_stock INT NOT NULL,
    product_picture VARCHAR(1000),
    price_id      INT           NOT NULL,
    category_id   INT           NOT NULL,
    FOREIGN KEY (price_id) REFERENCES price (price_id),
    FOREIGN KEY (category_id) REFERENCES category (category_id)
);
