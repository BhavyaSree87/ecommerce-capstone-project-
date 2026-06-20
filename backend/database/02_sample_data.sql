-- Insert sample users
INSERT INTO USERS (ID, NAME, EMAIL, PASSWORD, ROLE, MOBILE, ADDRESS, CITY, STATE, PINCODE)
VALUES (USER_SEQ.NEXTVAL, 'Admin User', 'admin@ecommerce.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUGyXlem', 'ADMIN', '9999999999', '123 Admin Street', 'Hyderabad', 'Telangana', '500001');

INSERT INTO USERS (ID, NAME, EMAIL, PASSWORD, ROLE, MOBILE, ADDRESS, CITY, STATE, PINCODE)
VALUES (USER_SEQ.NEXTVAL, 'John Doe', 'john@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUGyXlem', 'CUSTOMER', '9876543210', '456 Main Street', 'Bangalore', 'Karnataka', '560001');

INSERT INTO USERS (ID, NAME, EMAIL, PASSWORD, ROLE, MOBILE, ADDRESS, CITY, STATE, PINCODE)
VALUES (USER_SEQ.NEXTVAL, 'Jane Smith', 'jane@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUGyXlem', 'CUSTOMER', '8765432109', '789 Oak Avenue', 'Delhi', 'Delhi', '110001');

-- Insert sample products
INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Wireless Headphones', 2499.99, 'High-quality wireless headphones with noise cancellation', 'Electronics', 'Sony', 50, 'https://example.com/headphones.jpg', 4.5);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Smartphone', 29999.99, 'Latest model smartphone with advanced features', 'Electronics', 'Samsung', 30, 'https://example.com/smartphone.jpg', 4.7);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Running Shoes', 4999.99, 'Comfortable running shoes for daily use', 'Footwear', 'Nike', 100, 'https://example.com/shoes.jpg', 4.3);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'T-Shirt', 599.99, 'Cotton t-shirt available in multiple colors', 'Clothing', 'Levi''s', 200, 'https://example.com/tshirt.jpg', 4.1);

INSERT INTO PRODUCTS (PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING)
VALUES (PRODUCT_SEQ.NEXTVAL, 'Laptop', 79999.99, 'Powerful laptop for work and entertainment', 'Electronics', 'Dell', 20, 'https://example.com/laptop.jpg', 4.6);

COMMIT;
