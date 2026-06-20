from fastapi import APIRouter, HTTPException, Depends
from app.database.db import get_connection
from app.schemas.category_schema import CategoryCreate, CategoryUpdate
from app.utils.auth_dependency import admin_only
from app.logger import get_logger

logger = get_logger("category_routes")
router = APIRouter()


def serialize_category(row):
    return {
        "id": row[0],
        "category_name": row[1],
        "description": row[2],
    }


def ensure_category_schema(cursor):
    cursor.execute("SELECT COUNT(*) FROM user_tables WHERE table_name = 'CATEGORIES'")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            """
            CREATE TABLE CATEGORIES (
                CATEGORY_ID NUMBER PRIMARY KEY,
                CATEGORY_NAME VARCHAR2(150) NOT NULL UNIQUE,
                DESCRIPTION VARCHAR2(1000)
            )
            """
        )

    cursor.execute("SELECT COUNT(*) FROM user_sequences WHERE sequence_name = 'CATEGORY_SEQ'")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "CREATE SEQUENCE CATEGORY_SEQ START WITH 1 INCREMENT BY 1 NOCACHE"
        )


@router.get("/all", dependencies=[Depends(admin_only)])
def get_all_categories():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        ensure_category_schema(cursor)

        cursor.execute("SELECT CATEGORY_ID, CATEGORY_NAME, DESCRIPTION FROM CATEGORIES ORDER BY CATEGORY_NAME")
        rows = cursor.fetchall()
        if not rows:
            cursor.execute("SELECT DISTINCT CATEGORY FROM PRODUCTS WHERE CATEGORY IS NOT NULL ORDER BY CATEGORY")
            product_categories = cursor.fetchall()
            for category_row in product_categories:
                category_name = category_row[0]
                cursor.execute(
                    "INSERT INTO CATEGORIES (CATEGORY_ID, CATEGORY_NAME, DESCRIPTION) VALUES (CATEGORY_SEQ.NEXTVAL, :name, NULL)",
                    {"name": category_name},
                )
            conn.commit()
            cursor.execute("SELECT CATEGORY_ID, CATEGORY_NAME, DESCRIPTION FROM CATEGORIES ORDER BY CATEGORY_NAME")
            rows = cursor.fetchall()

        categories = [serialize_category(row) for row in rows]
        logger.info("Fetched %s categories", len(categories))
        return categories
    except Exception as e:
        logger.error(f"Get all categories failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve categories")
    finally:
        cursor.close()
        conn.close()


@router.post("/add", dependencies=[Depends(admin_only)])
def add_category(category: CategoryCreate):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        ensure_category_schema(cursor)

        cursor.execute(
            "SELECT CATEGORY_ID FROM CATEGORIES WHERE UPPER(CATEGORY_NAME) = UPPER(:name)",
            {"name": category.category_name},
        )
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Category already exists")

        cursor.execute("SELECT CATEGORY_SEQ.NEXTVAL FROM DUAL")
        category_id = cursor.fetchone()[0]

        cursor.execute(
            "INSERT INTO CATEGORIES (CATEGORY_ID, CATEGORY_NAME, DESCRIPTION) VALUES (:id, :name, :description)",
            {
                "id": category_id,
                "name": category.category_name,
                "description": category.description,
            },
        )
        conn.commit()

        return {
            "id": category_id,
            "category_name": category.category_name,
            "description": category.description,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Add category failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to add category")
    finally:
        cursor.close()
        conn.close()


@router.put("/update/{category_id}", dependencies=[Depends(admin_only)])
def update_category(category_id: int, category: CategoryUpdate):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        ensure_category_schema(cursor)

        cursor.execute(
            "SELECT CATEGORY_NAME, DESCRIPTION FROM CATEGORIES WHERE CATEGORY_ID = :id",
            {"id": category_id},
        )
        existing = cursor.fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="Category not found")

        existing_name, existing_description = existing
        new_name = category.category_name.strip() if category.category_name is not None else existing_name
        new_description = category.description if category.description is not None else existing_description

        if new_name.lower() != existing_name.lower():
            cursor.execute(
                "SELECT CATEGORY_ID FROM CATEGORIES WHERE UPPER(CATEGORY_NAME) = UPPER(:name) AND CATEGORY_ID != :id",
                {"name": new_name, "id": category_id},
            )
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Another category with this name already exists")

        cursor.execute(
            "UPDATE CATEGORIES SET CATEGORY_NAME = :name, DESCRIPTION = :description WHERE CATEGORY_ID = :id",
            {
                "name": new_name,
                "description": new_description,
                "id": category_id,
            },
        )

        if new_name != existing_name:
            cursor.execute(
                "UPDATE PRODUCTS SET CATEGORY = :new_name WHERE CATEGORY = :existing_name",
                {"new_name": new_name, "existing_name": existing_name},
            )

        conn.commit()

        return {
            "id": category_id,
            "category_name": new_name,
            "description": new_description,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update category failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to update category")
    finally:
        cursor.close()
        conn.close()


@router.delete("/delete/{category_id}", dependencies=[Depends(admin_only)])
def delete_category(category_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        ensure_category_schema(cursor)

        cursor.execute(
            "SELECT CATEGORY_NAME FROM CATEGORIES WHERE CATEGORY_ID = :id",
            {"id": category_id},
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Category not found")

        category_name = row[0]
        cursor.execute(
            "SELECT COUNT(*) FROM PRODUCTS WHERE CATEGORY = :category",
            {"category": category_name},
        )
        product_count = cursor.fetchone()[0]
        if product_count > 0:
            raise HTTPException(
                status_code=400,
                detail="Category cannot be deleted while products are using it",
            )

        cursor.execute("DELETE FROM CATEGORIES WHERE CATEGORY_ID = :id", {"id": category_id})
        conn.commit()

        return {"message": "Category deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete category failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete category")
    finally:
        cursor.close()
        conn.close()
