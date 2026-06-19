from fastapi import APIRouter, HTTPException, Query, Depends
from app.database.db import get_connection
from app.schemas.product_schema import ProductCreate, ProductOut, PaginatedProducts
from app.utils.auth_dependency import current_user, admin_only
from app.logger import get_logger
from typing import Optional

logger = get_logger("product_routes")
router = APIRouter()

# Add Product
@router.post("/add")
def add_product(
    product: ProductCreate,
    user = Depends(admin_only)
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO PRODUCTS
        (
            PRODUCT_ID,
            PRODUCT_NAME,
            PRICE,
            DESCRIPTION,
            CATEGORY,
            BRAND,
            STOCK,
            IMAGE_URL,
            RATING
        )
        VALUES
        (
            PRODUCT_SEQ.NEXTVAL,
            :product_name,
            :price,
            :description,
            :category,
            :brand,
            :stock,
            :image_url,
            :rating
        )
    """,
    {
        "product_name": product.product_name,
        "price": product.price,
        "description": product.description,
        "category": product.category,
        "brand": product.brand,
        "stock": product.stock,
        "image_url": product.image_url,
        "rating": product.rating
    })

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Product Added Successfully"
    }


@router.get("/all", response_model=PaginatedProducts)
def get_all_products(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        
        cursor.execute("SELECT COUNT(*) FROM PRODUCTS")
        total = cursor.fetchone()[0]

        start = (page - 1) * page_size + 1
        end = page * page_size

        
        cursor.execute(
            f"""
            SELECT * FROM (
                SELECT a.*, ROWNUM rnum FROM (
                    SELECT PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING FROM PRODUCTS ORDER BY PRODUCT_ID DESC
                ) a WHERE ROWNUM <= {end}
            ) WHERE rnum >= {start}
            """
        )
        rows = cursor.fetchall()

        items = [
            ProductOut(
                product_id=r[0],
                product_name=r[1],
                price=r[2],
                description=r[3],
                category=r[4],
                brand=r[5],
                stock=r[6],
                image_url=r[7],
                rating=r[8],
            )
            for r in rows
        ]

        return {"total": total, "page": page, "page_size": page_size, "items": items}
    except Exception as e:
        import traceback
        traceback.print_exc()
        # return detailed error for debugging
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()



@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING
            FROM PRODUCTS
            WHERE PRODUCT_ID = :id
            """,
            {"id": product_id}
        )
        product = cursor.fetchone()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        return {
            "product_id": product[0],
            "product_name": product[1],
            "price": product[2],
            "description": product[3],
            "category": product[4],
            "brand": product[5],
            "stock": product[6],
            "image_url": product[7],
            "rating": product[8]
        }
    except Exception as e:
        logger.error(f"Get product failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve product")
    finally:
        cursor.close()
        conn.close()



@router.delete("/delete/{product_id}")
def delete_product(
    product_id: int,
    user = Depends(admin_only)
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM PRODUCTS WHERE PRODUCT_ID=:id",
        {"id": product_id}
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Product Deleted Successfully"
    }
    
@router.put("/update/{product_id}", dependencies=[Depends(admin_only)])
def update_product(product_id: int, product: ProductCreate):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT PRODUCT_ID FROM PRODUCTS WHERE PRODUCT_ID = :id", {"id": product_id})
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Product not found")

        cursor.execute("""
            UPDATE PRODUCTS
            SET
                PRODUCT_NAME = :product_name,
                PRICE = :price,
                DESCRIPTION = :description,
                CATEGORY = :category,
                BRAND = :brand,
                STOCK = :stock,
                IMAGE_URL = :image_url,
                RATING = :rating
            WHERE PRODUCT_ID = :product_id
        """,
        {
            "product_name": product.product_name,
            "price": product.price,
            "description": product.description,
            "category": product.category,
            "brand": product.brand,
            "stock": product.stock,
            "image_url": product.image_url,
            "rating": product.rating,
            "product_id": product_id
        })
        conn.commit()
        return {"message": "Product Updated Successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update product failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to update product")
    finally:
        cursor.close()
        conn.close()
    
@router.get("/search/{name}", response_model=PaginatedProducts)
def search_product(name: str, page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM PRODUCTS WHERE UPPER(PRODUCT_NAME) LIKE UPPER(:name)", {"name": f"%{name}%"})
        total = cursor.fetchone()[0]

        start = (page - 1) * page_size + 1
        end = page * page_size

        cursor.execute(
            f"""
            SELECT * FROM (
                SELECT a.*, ROWNUM rnum FROM (
                    SELECT PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING FROM PRODUCTS
                    WHERE UPPER(PRODUCT_NAME) LIKE UPPER(:name) ORDER BY PRODUCT_ID DESC
                ) a WHERE ROWNUM <= {end}
            ) WHERE rnum >= {start}
            """,
            {"name": f"%{name}%"},
        )
        rows = cursor.fetchall()
        items = [
            ProductOut(
                product_id=r[0],
                product_name=r[1],
                price=r[2],
                description=r[3],
                category=r[4],
                brand=r[5],
                stock=r[6],
                image_url=r[7],
                rating=r[8],
            )
            for r in rows
        ]
        return {"total": total, "page": page, "page_size": page_size, "items": items}
    except Exception as e:
        logger.error(f"Search products failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to search products")
    finally:
        cursor.close()
        conn.close()

@router.get("/category/{category}", response_model=PaginatedProducts)
def get_by_category(category: str, page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM PRODUCTS WHERE UPPER(CATEGORY) = UPPER(:category)", {"category": category})
        total = cursor.fetchone()[0]

        start = (page - 1) * page_size + 1
        end = page * page_size

        cursor.execute(
            f"""
            SELECT * FROM (
                SELECT a.*, ROWNUM rnum FROM (
                    SELECT PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING FROM PRODUCTS
                    WHERE UPPER(CATEGORY) = UPPER(:category) ORDER BY PRODUCT_ID DESC
                ) a WHERE ROWNUM <= {end}
            ) WHERE rnum >= {start}
            """,
            {"category": category},
        )
        rows = cursor.fetchall()
        items = [
            ProductOut(
                product_id=r[0],
                product_name=r[1],
                price=r[2],
                description=r[3],
                category=r[4],
                brand=r[5],
                stock=r[6],
                image_url=r[7],
                rating=r[8],
            )
            for r in rows
        ]
        return {"total": total, "page": page, "page_size": page_size, "items": items}
    except Exception as e:
        logger.error(f"Get by category failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve products by category")
    finally:
        cursor.close()
        conn.close()

@router.get("/brand/{brand}")
def get_by_brand(brand: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM PRODUCTS
        WHERE BRAND = :brand
    """,
    {
        "brand": brand
    })

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data

@router.get("/price/{min_price}/{max_price}")
def filter_price(
    min_price: int,
    max_price: int
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM PRODUCTS
        WHERE PRICE
        BETWEEN :min_price
        AND :max_price
        """,
        {
            "min_price": min_price,
            "max_price": max_price
        }
    )

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data