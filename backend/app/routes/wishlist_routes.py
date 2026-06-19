from fastapi import APIRouter, Depends, HTTPException
from app.database.db import get_connection
from app.schemas.wishlist_schema import WishlistCreate
from app.utils.auth_dependency import current_user

router = APIRouter()


@router.post("/add")
def add_wishlist(item: WishlistCreate, user=Depends(current_user)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO WISHLIST (WISHLIST_ID, USER_ID, PRODUCT_ID) VALUES (WISHLIST_SEQ.NEXTVAL, :user_id, :product_id)",
            {"user_id": user.get("user_id"), "product_id": item.product_id},
        )
        conn.commit()
        return {"message": "Added To Wishlist"}
    finally:
        cursor.close()
        conn.close()


@router.get("/")
def get_wishlist(user=Depends(current_user)):
    user_id = user.get("user_id")
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT WISHLIST_ID, USER_ID, PRODUCT_ID FROM WISHLIST WHERE USER_ID = :id", {"id": user_id})
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()
        conn.close()


@router.delete("/delete/{wishlist_id}")
def delete_wishlist(wishlist_id: int, user=Depends(current_user)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT USER_ID FROM WISHLIST WHERE WISHLIST_ID = :id", {"id": wishlist_id})
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Wishlist item not found")
        if row[0] != user.get("user_id") and user.get("role") != "ADMIN":
            raise HTTPException(status_code=403, detail="Access denied")
        cursor.execute("DELETE FROM WISHLIST WHERE WISHLIST_ID = :id", {"id": wishlist_id})
        conn.commit()
        return {"message": "Wishlist Item Deleted"}
    finally:
        cursor.close()
        conn.close()