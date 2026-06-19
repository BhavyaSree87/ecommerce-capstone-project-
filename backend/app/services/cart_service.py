"""Cart service - handles shopping cart operations"""

from app.database.db import get_db_context
from app.exceptions import ResourceNotFoundError, ValidationError, DatabaseError
from app.logger import get_logger
from typing import Dict, List

logger = get_logger("cart_service")


class CartService:
    """Service class for cart operations"""
    
    @staticmethod
    def add_to_cart(user_id: int, product_id: int, quantity: int) -> Dict:
        """Add item to cart"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                cursor.execute(
                    """
                    INSERT INTO CART (CART_ID, USER_ID, PRODUCT_ID, QUANTITY)
                    VALUES (CART_SEQ.NEXTVAL, :user_id, :product_id, :quantity)
                    """,
                    {"user_id": user_id, "product_id": product_id, "quantity": quantity}
                )
                
                logger.info(f"Item {product_id} added to cart for user {user_id}")
                return {"message": "Item added to cart"}
                
        except Exception as e:
            logger.error(f"Add to cart failed: {e}")
            raise DatabaseError("Add to cart failed")
    
    @staticmethod
    def get_cart(user_id: int) -> Dict:
        """Get user's cart"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                cursor.execute(
                    """
                    SELECT CART_ID, USER_ID, PRODUCT_ID, QUANTITY 
                    FROM CART WHERE USER_ID = :id
                    """,
                    {"id": user_id}
                )
                
                items = []
                for row in cursor.fetchall():
                    items.append({
                        "cart_id": row[0],
                        "user_id": row[1],
                        "product_id": row[2],
                        "quantity": row[3]
                    })
                
                return {
                    "total_items": len(items),
                    "items": items
                }
        except Exception as e:
            logger.error(f"Get cart failed: {e}")
            raise DatabaseError("Get cart failed")
    
    @staticmethod
    def remove_from_cart(cart_id: int, user_id: int) -> Dict:
        """Remove item from cart"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                # Verify ownership
                cursor.execute(
                    "SELECT USER_ID FROM CART WHERE CART_ID = :id",
                    {"id": cart_id}
                )
                row = cursor.fetchone()
                
                if not row:
                    raise ResourceNotFoundError("Cart item", cart_id)
                
                if row[0] != user_id:
                    raise ValidationError("Unauthorized access to cart item")
                
                cursor.execute("DELETE FROM CART WHERE CART_ID = :id", {"id": cart_id})
                
                logger.info(f"Cart item {cart_id} removed for user {user_id}")
                return {"message": "Item removed from cart"}
                
        except (ResourceNotFoundError, ValidationError):
            raise
        except Exception as e:
            logger.error(f"Remove from cart failed: {e}")
            raise DatabaseError("Remove from cart failed")
    
    @staticmethod
    def clear_cart(user_id: int) -> Dict:
        """Clear user's cart"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM CART WHERE USER_ID = :id", {"id": user_id})
                
                logger.info(f"Cart cleared for user {user_id}")
                return {"message": "Cart cleared"}
                
        except Exception as e:
            logger.error(f"Clear cart failed: {e}")
            raise DatabaseError("Clear cart failed")
