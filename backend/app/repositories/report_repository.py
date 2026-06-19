from datetime import datetime
from app.logger import get_logger

logger = get_logger("report_repository")


def get_dashboard_counts(cursor):
    query = """
        SELECT
            (SELECT COUNT(*) FROM USERS) AS TOTAL_USERS,
            (SELECT COUNT(*) FROM PRODUCTS) AS TOTAL_PRODUCTS,
            (SELECT COUNT(DISTINCT ORDER_ID) FROM ORDERS) AS TOTAL_ORDERS,
            (SELECT COUNT(*) FROM PAYMENTS) AS TOTAL_PAYMENTS,
            NVL((SELECT SUM(AMOUNT) FROM PAYMENTS WHERE PAYMENT_STATUS = 'SUCCESS'), 0) AS TOTAL_REVENUE,
            (SELECT COUNT(DISTINCT ORDER_ID) FROM ORDERS WHERE STATUS = 'PENDING') AS PENDING_ORDERS,
            (SELECT COUNT(DISTINCT ORDER_ID) FROM ORDERS WHERE STATUS = 'DELIVERED') AS COMPLETED_ORDERS
        FROM DUAL
        """
    logger.info("Executing dashboard counts query")
    logger.info("SQL: %s", query)
    try:
        cursor.execute(query)
        row = cursor.fetchone()
        logger.info("Dashboard counts query completed: %s", row)
        return row
    except Exception:
        logger.exception("Dashboard counts SQL Error")
        raise


def get_top_selling_products(cursor):
    query = """
        SELECT p.PRODUCT_ID, p.PRODUCT_NAME, SUM(o.QUANTITY) AS TOTAL_QUANTITY_SOLD
        FROM ORDERS o
        JOIN PRODUCTS p ON o.PRODUCT_ID = p.PRODUCT_ID
        GROUP BY p.PRODUCT_ID, p.PRODUCT_NAME
        ORDER BY TOTAL_QUANTITY_SOLD DESC
        """
    logger.info("Executing top-selling products query")
    logger.info("SQL: %s", query)
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        logger.info("Top-selling products query completed: %s rows", len(rows))
        return rows
    except Exception:
        logger.exception("Top-selling products SQL Error")
        raise


def get_monthly_revenue(cursor):
    query = """
        SELECT TO_CHAR(TRUNC(o.CREATED_AT, 'MM'), 'YYYY-MM') AS MONTH, NVL(SUM(p.AMOUNT), 0) AS REVENUE
        FROM PAYMENTS p
        LEFT JOIN ORDERS o ON p.ORDER_ID = o.ORDER_ID
        WHERE p.PAYMENT_STATUS = 'SUCCESS'
          AND o.ORDER_ID IS NOT NULL
        GROUP BY TRUNC(o.CREATED_AT, 'MM')
        ORDER BY TRUNC(o.CREATED_AT, 'MM')
        """
    logger.info("Executing monthly revenue query")
    logger.info("SQL: %s", query)
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        logger.info("Monthly revenue query completed: %s rows", len(rows))
        return rows
    except Exception:
        logger.exception("Monthly revenue SQL Error")
        raise


def get_low_stock_products(cursor):
    query = """
        SELECT PRODUCT_ID, PRODUCT_NAME, STOCK
        FROM PRODUCTS
        WHERE STOCK < 10
        ORDER BY STOCK ASC, PRODUCT_ID DESC
        """
    logger.info("Executing low stock products query")
    logger.info("SQL: %s", query)
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        logger.info("Low stock products query completed: %s rows", len(rows))
        return rows
    except Exception:
        logger.exception("Low stock products SQL Error")
        raise


def get_payment_summary(cursor):
    query = """
        SELECT
            COUNT(*) TOTAL_PAYMENTS,
            NVL(SUM(CASE WHEN PAYMENT_STATUS IN ('SUCCESS', 'PAID') THEN 1 ELSE 0 END), 0) SUCCESSFUL_PAYMENTS,
            NVL(SUM(CASE WHEN PAYMENT_STATUS = 'PENDING' THEN 1 ELSE 0 END), 0) PENDING_PAYMENTS,
            NVL(SUM(CASE WHEN PAYMENT_STATUS = 'FAILED' THEN 1 ELSE 0 END), 0) FAILED_PAYMENTS,
            NVL(SUM(AMOUNT), 0) TOTAL_AMOUNT
        FROM PAYMENTS
        """
    logger.info("Executing payment summary query")
    logger.info("SQL: %s", query)
    try:
        cursor.execute(query)
        row = cursor.fetchone()
        logger.info("Payment summary query completed: %s", row)
        return row
    except Exception:
        logger.exception("Payment summary SQL Error")
        raise
