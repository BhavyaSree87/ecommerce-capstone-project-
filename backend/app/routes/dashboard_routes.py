from fastapi import APIRouter, Depends
from app.database.db import get_connection
from app.utils.auth_dependency import admin_only
from app.logger import get_logger

logger = get_logger("dashboard_routes")

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)


@router.get("/stats", dependencies=[Depends(admin_only)])
def dashboard_stats():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM USERS")
        users = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM PRODUCTS")
        products = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT ORDER_ID) FROM ORDERS")
        orders = cursor.fetchone()[0]

        cursor.execute("""
            SELECT NVL(SUM(AMOUNT), 0) 
            FROM PAYMENTS 
            WHERE PAYMENT_STATUS IN ('SUCCESS', 'PAID')
        """)
        total_revenue = float(cursor.fetchone()[0] or 0)

        cursor.execute("SELECT COUNT(*) FROM PRODUCTS WHERE STOCK < 10")
        low_stock = cursor.fetchone()[0]

        logger.info("Dashboard stats retrieved successfully")
        return {
            "total_users": users,
            "total_products": products,
            "total_orders": orders,
            "total_revenue": total_revenue,
            "low_stock_products": low_stock
        }
    except Exception as e:
        logger.error(f"Dashboard stats failed: {e}")
        raise
    finally:
        cursor.close()
        conn.close()
    
