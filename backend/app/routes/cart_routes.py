from fastapi import APIRouter, Depends, HTTPException
from app.database.db import get_connection
from app.schemas.cart_schema import CartCreate
from app.utils.auth_dependency import current_user

router = APIRouter()


@router.post("/add")
def add_cart(cart: CartCreate, user=Depends(current_user)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO CART (CART_ID, USER_ID, PRODUCT_ID, QUANTITY)
            VALUES (CART_SEQ.NEXTVAL, :user_id, :product_id, :quantity)
            """,
            {"user_id": user.get("user_id"), "product_id": cart.product_id, "quantity": cart.quantity},
        )
        conn.commit()
        return {"message": "Item Added To Cart"}
    finally:
        cursor.close()
        conn.close()


@router.get("/")
def get_cart(user=Depends(current_user)):
    user_id = user.get("user_id")
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT CART_ID, USER_ID, PRODUCT_ID, QUANTITY FROM CART WHERE USER_ID = :id", {"id": user_id})
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()
        conn.close()


@router.delete("/delete/{cart_id}")
def delete_cart(cart_id: int, user=Depends(current_user)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        
        cursor.execute("SELECT USER_ID FROM CART WHERE CART_ID = :id", {"id": cart_id})
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Cart item not found")
        if row[0] != user.get("user_id") and user.get("role") != "ADMIN":
            raise HTTPException(status_code=403, detail="Access denied")
        cursor.execute("DELETE FROM CART WHERE CART_ID = :id", {"id": cart_id})
        conn.commit()
        return {"message": "Cart Item Deleted"}
    finally:
        cursor.close()
        conn.close()