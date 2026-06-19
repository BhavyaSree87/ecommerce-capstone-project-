from fastapi import APIRouter, HTTPException, Depends
from app.database.db import get_connection
from app.schemas.report_schema import (
    DashboardReport,
    TopSellingProduct,
    MonthlyRevenueItem,
    LowStockProduct,
    PaymentSummary,
)
from app.services.report_service import ReportService
from app.utils.auth_dependency import admin_only
from app.logger import get_logger

logger = get_logger("report_routes")
router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/dashboard", response_model=DashboardReport, summary="Get platform dashboard analytics")
def dashboard_report(user=Depends(admin_only)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        report = ReportService.get_dashboard_summary(cursor)
        logger.info("Dashboard analytics fetched successfully")
        return report
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Dashboard analytics fetch failed: {exc}")
        raise HTTPException(status_code=500, detail="Unable to fetch dashboard analytics")
    finally:
        cursor.close()
        conn.close()


@router.get("/top-selling-products", response_model=list[TopSellingProduct], summary="Get top selling products by quantity")
def top_selling_products(user=Depends(admin_only)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        products = ReportService.get_top_selling_products(cursor)
        logger.info("Top-selling products fetched successfully")
        return products
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Top-selling products fetch failed: {exc}")
        raise HTTPException(status_code=500, detail="Unable to fetch top-selling products")
    finally:
        cursor.close()
        conn.close()


@router.get("/monthly-revenue", response_model=list[MonthlyRevenueItem], summary="Get monthly revenue summary")
def monthly_revenue(user=Depends(admin_only)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        revenue = ReportService.get_monthly_revenue(cursor)
        logger.info("Monthly revenue fetched successfully")
        return revenue
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Monthly revenue fetch failed: {exc}")
        raise HTTPException(status_code=500, detail="Unable to fetch monthly revenue")
    finally:
        cursor.close()
        conn.close()


@router.get("/low-stock", response_model=list[LowStockProduct], summary="Get products with low stock")
def low_stock_report(user=Depends(admin_only)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        products = ReportService.get_low_stock_products(cursor)
        logger.info("Low stock report fetched successfully")
        return products
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Low stock report fetch failed: {exc}")
        raise HTTPException(status_code=500, detail="Unable to fetch low stock products")
    finally:
        cursor.close()
        conn.close()


@router.get("/payment-summary", response_model=PaymentSummary, summary="Get payment status summary")
def payment_summary(user=Depends(admin_only)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        summary = ReportService.get_payment_summary(cursor)
        logger.info("Payment summary fetched successfully")
        return summary
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Payment summary fetch failed: {exc}")
        raise HTTPException(status_code=500, detail="Unable to fetch payment summary")
    finally:
        cursor.close()
        conn.close()
