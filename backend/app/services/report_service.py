from app.repositories.report_repository import (
    get_dashboard_counts,
    get_top_selling_products,
    get_monthly_revenue,
    get_low_stock_products,
    get_payment_summary,
)
from app.logger import get_logger
from app.exceptions import DatabaseError

logger = get_logger("report_service")


class ReportService:
    @staticmethod
    def get_dashboard_summary(cursor):
        row = get_dashboard_counts(cursor)
        if not row:
            logger.error("Dashboard counts query returned no results")
            raise DatabaseError("Failed to retrieve dashboard analytics")

        return {
            "total_users": row[0],
            "total_products": row[1],
            "total_orders": row[2],
            "total_payments": row[3],
            "total_revenue": float(row[4] or 0),
            "pending_orders": row[5],
            "completed_orders": row[6],
        }

    @staticmethod
    def get_top_selling_products(cursor):
        rows = get_top_selling_products(cursor)
        return [
            {
                "product_id": row[0],
                "product_name": row[1],
                "total_quantity_sold": row[2],
            }
            for row in rows
        ]

    @staticmethod
    def get_monthly_revenue(cursor):
        rows = get_monthly_revenue(cursor)
        return [
            {
                "month": row[0],
                "revenue": float(row[1] or 0),
            }
            for row in rows
        ]

    @staticmethod
    def get_low_stock_products(cursor):
        rows = get_low_stock_products(cursor)
        return [
            {
                "product_id": row[0],
                "product_name": row[1],
                "stock": row[2],
            }
            for row in rows
        ]

    @staticmethod
    def get_payment_summary(cursor):
        row = get_payment_summary(cursor)
        if not row:
            logger.error("Payment summary query returned no results")
            raise DatabaseError("Failed to retrieve payment summary")

        return {
            "total_payments": row[0],
            "successful_payments": row[1],
            "pending_payments": row[2],
            "failed_payments": row[3],
            "total_amount": float(row[4] or 0),
        }
