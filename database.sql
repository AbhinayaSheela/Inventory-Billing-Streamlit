CREATE DATABASE shop_db;
USE shop_db;

CREATE TABLE products(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    price FLOAT,
    stock INT
);

CREATE TABLE bills(
    id INT AUTO_INCREMENT PRIMARY KEY,
    bill_date DATE,
    total_amount FLOAT
);

CREATE TABLE bill_items(
    id INT AUTO_INCREMENT PRIMARY KEY,
    bill_id INT,
    product_id INT,
    quantity INT,
    FOREIGN KEY (bill_id) REFERENCES bills(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Sample data
INSERT INTO products(name, price, stock)
VALUES
('Pen', 10, 100),
('Book', 50, 60),
('Bag', 500, 20);
