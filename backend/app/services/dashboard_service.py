"""Dashboard service - provides analytics and statistics"""

from app.database.db import get_db_context
from app.exceptions import DatabaseError
from app.logger import get_logger
from typing import Dict

logger = get_logger("dashboard_service")


class DashboardService:
    """Service class for dashboard analytics"""
    
    @staticmethod
    def get_dashboard_stats() -> Dict:
        """Get comprehensive dashboard statistics"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                # Get user count
                cursor.execute("SELECT COUNT(*) FROM USERS")
                total_users = cursor.fetchone()[0]
                
                # Get product count
                cursor.execute("SELECT COUNT(*) FROM PRODUCTS")
                total_products = cursor.fetchone()[0]
                
                # Get order count
                cursor.execute("SELECT COUNT(DISTINCT ORDER_ID) FROM ORDERS")
                total_orders = cursor.fetchone()[0]
                
                # Get payment count
                cursor.execute("SELECT COUNT(*) FROM PAYMENTS")
                total_payments = cursor.fetchone()[0]
                
                # Calculate total revenue
                cursor.execute(
                    "SELECT NVL(SUM(AMOUNT), 0) FROM PAYMENTS WHERE PAYMENT_STATUS = 'SUCCESS'"
                )
                total_revenue = cursor.fetchone()[0]
                
                # Get top selling products
                cursor.execute(
                    """
                    SELECT PRODUCT_ID, SUM(QUANTITY) as total_sold
                    FROM ORDERS WHERE STATUS != 'CANCELLED'
                    GROUP BY PRODUCT_ID
                    ORDER BY total_sold DESC
                    FETCH FIRST 5 ROWS ONLY
                    """
                )
                
                top_products = []
                for row in cursor.fetchall():
                    top_products.append({
                        "product_id": row[0],
                        "total_sold": row[1]
                    })
                
                # Get pending orders
                cursor.execute(
                    "SELECT COUNT(DISTINCT ORDER_ID) FROM ORDERS WHERE STATUS = 'PENDING'"
                )
                pending_orders = cursor.fetchone()[0]
                
                # Get failed payments
                cursor.execute(
                    "SELECT COUNT(*) FROM PAYMENTS WHERE PAYMENT_STATUS = 'FAILED'"
                )
                failed_payments = cursor.fetchone()[0]
                
                logger.info("Dashboard stats retrieved")
                
                return {
                    "total_users": total_users,
                    "total_products": total_products,
                    "total_orders": total_orders,
                    "total_payments": total_payments,
                    "total_revenue": float(total_revenue),
                    "pending_orders": pending_orders,
                    "failed_payments": failed_payments,
                    "top_selling_products": top_products
                }
        except Exception as e:
            logger.error(f"Get dashboard stats failed: {e}")
            raise DatabaseError("Dashboard stats retrieval failed")
