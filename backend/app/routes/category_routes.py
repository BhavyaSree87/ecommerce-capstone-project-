from fastapi import APIRouter, Depends
from app.database.db import get_connection
from app.utils.auth_dependency import admin_only
from app.logger import get_logger

logger = get_logger("category_routes")
router = APIRouter()

@router.get("/all", dependencies=[Depends(admin_only)])
def get_all_categories():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT DISTINCT CATEGORY FROM PRODUCTS ORDER BY CATEGORY")
        rows = cursor.fetchall()
        categories = [
            {"id": idx + 1, "category_name": row[0], "description": None}
            for idx, row in enumerate(rows)
        ]
        logger.info("Fetched %s categories", len(categories))
        return categories
    finally:
        cursor.close()
        conn.close()
