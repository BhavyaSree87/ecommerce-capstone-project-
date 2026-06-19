"""Wishlist service - handles wishlist operations"""

from app.database.db import get_db_context
from app.exceptions import ResourceNotFoundError, ValidationError, DatabaseError
from app.logger import get_logger
from typing import Dict

logger = get_logger("wishlist_service")


class WishlistService:
    """Service class for wishlist operations"""
    
    @staticmethod
    def add_to_wishlist(user_id: int, product_id: int) -> Dict:
        """Add item to wishlist"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                cursor.execute(
                    """
                    INSERT INTO WISHLIST (WISHLIST_ID, USER_ID, PRODUCT_ID)
                    VALUES (WISHLIST_SEQ.NEXTVAL, :user_id, :product_id)
                    """,
                    {"user_id": user_id, "product_id": product_id}
                )
                
                logger.info(f"Product {product_id} added to wishlist for user {user_id}")
                return {"message": "Added to wishlist"}
                
        except Exception as e:
            logger.error(f"Add to wishlist failed: {e}")
            raise DatabaseError("Add to wishlist failed")
    
    @staticmethod
    def get_wishlist(user_id: int) -> Dict:
        """Get user's wishlist"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                cursor.execute(
                    """
                    SELECT WISHLIST_ID, USER_ID, PRODUCT_ID
                    FROM WISHLIST WHERE USER_ID = :id
                    """,
                    {"id": user_id}
                )
                
                items = []
                for row in cursor.fetchall():
                    items.append({
                        "wishlist_id": row[0],
                        "user_id": row[1],
                        "product_id": row[2]
                    })
                
                return {
                    "total_items": len(items),
                    "items": items
                }
        except Exception as e:
            logger.error(f"Get wishlist failed: {e}")
            raise DatabaseError("Get wishlist failed")
    
    @staticmethod
    def remove_from_wishlist(wishlist_id: int, user_id: int) -> Dict:
        """Remove item from wishlist"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                # Verify ownership
                cursor.execute(
                    "SELECT USER_ID FROM WISHLIST WHERE WISHLIST_ID = :id",
                    {"id": wishlist_id}
                )
                row = cursor.fetchone()
                
                if not row:
                    raise ResourceNotFoundError("Wishlist item", wishlist_id)
                
                if row[0] != user_id:
                    raise ValidationError("Unauthorized access to wishlist item")
                
                cursor.execute(
                    "DELETE FROM WISHLIST WHERE WISHLIST_ID = :id",
                    {"id": wishlist_id}
                )
                
                logger.info(f"Wishlist item {wishlist_id} removed for user {user_id}")
                return {"message": "Wishlist item deleted"}
                
        except (ResourceNotFoundError, ValidationError):
            raise
        except Exception as e:
            logger.error(f"Remove from wishlist failed: {e}")
            raise DatabaseError("Remove from wishlist failed")
    
    @staticmethod
    def clear_wishlist(user_id: int) -> Dict:
        """Clear user's wishlist"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                cursor.execute(
                    "DELETE FROM WISHLIST WHERE USER_ID = :id",
                    {"id": user_id}
                )
                
                logger.info(f"Wishlist cleared for user {user_id}")
                return {"message": "Wishlist cleared"}
                
        except Exception as e:
            logger.error(f"Clear wishlist failed: {e}")
            raise DatabaseError("Clear wishlist failed")
