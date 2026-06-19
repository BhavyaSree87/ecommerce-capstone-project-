-- Oracle 11g database objects for capstone reporting and order processing
-- Includes views, stored procedures, and validation queries.

-- 1. Top selling products view
CREATE OR REPLACE VIEW VW_TOP_SELLING_PRODUCTS AS
SELECT
    p.PRODUCT_ID,
    p.PRODUCT_NAME,
    NVL(SUM(o.QUANTITY), 0) AS TOTAL_QUANTITY_SOLD
FROM ORDERS o
JOIN PRODUCTS p ON o.PRODUCT_ID = p.PRODUCT_ID
GROUP BY p.PRODUCT_ID, p.PRODUCT_NAME;

-- 2. Monthly revenue view
CREATE OR REPLACE VIEW VW_MONTHLY_REVENUE AS
SELECT
    TO_CHAR(TRUNC(o.CREATED_AT, 'MM'), 'YYYY-MM') AS MONTH,
    NVL(SUM(p.AMOUNT), 0) AS TOTAL_REVENUE
FROM ORDERS o
JOIN PAYMENTS p ON p.ORDER_ID = o.ORDER_ID
WHERE p.PAYMENT_STATUS IN ('SUCCESS', 'PAID')
GROUP BY TRUNC(o.CREATED_AT, 'MM');

-- 3. Stock update stored procedure
CREATE OR REPLACE PROCEDURE SP_UPDATE_STOCK(
    p_product_id IN NUMBER,
    p_quantity IN NUMBER
)
AS
    v_stock NUMBER;
BEGIN
    IF p_quantity IS NULL OR p_quantity <= 0 THEN
        RAISE_APPLICATION_ERROR(-20001, 'Quantity must be greater than zero.');
    END IF;

    SELECT STOCK
    INTO v_stock
    FROM PRODUCTS
    WHERE PRODUCT_ID = p_product_id;

    IF v_stock < p_quantity THEN
        RAISE_APPLICATION_ERROR(-20002, 'Insufficient stock for product ' || p_product_id || '.');
    END IF;

    UPDATE PRODUCTS
    SET STOCK = STOCK - p_quantity
    WHERE PRODUCT_ID = p_product_id;

    IF SQL%ROWCOUNT = 0 THEN
        RAISE_APPLICATION_ERROR(-20003, 'Product not found: ' || p_product_id || '.');
    END IF;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20003, 'Product not found: ' || p_product_id || '.');
    WHEN OTHERS THEN
        RAISE_APPLICATION_ERROR(-20004, 'SP_UPDATE_STOCK failed: ' || SQLERRM);
END SP_UPDATE_STOCK;
/

-- 4. Place order stored procedure
CREATE OR REPLACE PROCEDURE SP_PLACE_ORDER(
    p_user_id IN NUMBER,
    p_product_id IN NUMBER,
    p_quantity IN NUMBER
)
AS
    v_price NUMBER;
    v_stock NUMBER;
    v_order_id NUMBER;
    v_item_id NUMBER;
BEGIN
    IF p_quantity IS NULL OR p_quantity <= 0 THEN
        RAISE_APPLICATION_ERROR(-20011, 'Order quantity must be greater than zero.');
    END IF;

    SELECT PRICE, STOCK
    INTO v_price, v_stock
    FROM PRODUCTS
    WHERE PRODUCT_ID = p_product_id;

    IF v_stock < p_quantity THEN
        RAISE_APPLICATION_ERROR(-20012, 'Insufficient stock for product ' || p_product_id || '.');
    END IF;

    SELECT ORDERS_SEQ.NEXTVAL INTO v_order_id FROM DUAL;
    SELECT ORDERS_SEQ.NEXTVAL INTO v_item_id FROM DUAL;

    INSERT INTO ORDERS (
        ORDER_ID,
        ITEM_ID,
        PRODUCT_ID,
        QUANTITY,
        PRICE,
        STATUS,
        USER_ID
    ) VALUES (
        v_order_id,
        v_item_id,
        p_product_id,
        p_quantity,
        v_price,
        'PENDING',
        p_user_id
    );

    SP_UPDATE_STOCK(p_product_id, p_quantity);
    COMMIT;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        ROLLBACK;
        RAISE_APPLICATION_ERROR(-20013, 'Product not found: ' || p_product_id || '.');
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE_APPLICATION_ERROR(-20014, 'SP_PLACE_ORDER failed: ' || SQLERRM);
END SP_PLACE_ORDER;
/

-- Validation queries
-- 1. Verify top selling products view
SELECT * FROM VW_TOP_SELLING_PRODUCTS;

-- 2. Verify monthly revenue view
SELECT * FROM VW_MONTHLY_REVENUE;

-- 3. Test stock update procedure
BEGIN
    SP_UPDATE_STOCK(1, 1);
END;
/

-- 4. Test place order procedure
BEGIN
    SP_PLACE_ORDER(1, 1, 1);
END;
/
-- 5. Confirm inserted order and updated stock
SELECT * FROM ORDERS WHERE ORDER_ID = (SELECT MAX(ORDER_ID) FROM ORDERS);
SELECT PRODUCT_ID, STOCK FROM PRODUCTS WHERE PRODUCT_ID = 1;
