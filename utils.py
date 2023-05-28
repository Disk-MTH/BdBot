import datetime


def mdp(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS category
        (
            category_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name VARCHAR(1000) NOT NULL
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS price
        (
            price_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            buy_price  DOUBLE,
            sell_price DOUBLE
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS product
        (
            product_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name  VARCHAR(1000) NOT NULL,
            product_stock INT,
            product_picture,
            price_id      INT           NOT NULL,
            category_id   INT           NOT NULL,
            FOREIGN KEY (price_id) REFERENCES price (price_id),
            FOREIGN KEY (category_id) REFERENCES category (category_id)
        );
        """
    )


def get_date_time():
    date = datetime.datetime.now()
    return date.strftime("%d/%m/%Y") + "-" + date.strftime("%H:%M:%S")
