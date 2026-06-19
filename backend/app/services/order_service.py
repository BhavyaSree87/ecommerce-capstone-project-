"""Order service - handles order-related business logic with inventory management"""

from app.database.db import get_db_context
from app.services.product_service import ProductService
from app.exceptions import (
    ResourceNotFoundError, ValidationError, DatabaseError,
    InsufficientStockError
)
from app.logger import get_logger
from typing import Dict, List, Optional
from datetime import datetime

logger = get_logger("order_service")


class OrderService:
    """Service class for order operations"""
    
    @staticmethod
    def create_order(user_id: int, order_data: Dict) -> Dict:
        """
        Create a new order with inventory management
        
        Args:
            user_id: User ID placing the order
            order_data: Dictionary with order details and items
            
        Returns:
            Created order details
            
        Raises:
            InsufficientStockError: If product stock is insufficient
            ValidationError: If order data is invalid
            DatabaseError: If database operation fails
        """
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                if not order_data.get('items'):
                    raise ValidationError("Order must contain at least one item")
                
                # Generate order ID
                cursor.execute("SELECT ORDERS_SEQ.NEXTVAL FROM DUAL")
                order_id = cursor.fetchone()[0]
                
                items_out = []
                total_amount = 0
                
                # Process each item
                for item in order_data['items']:
                    product_id = item.get('product_id')
                    quantity = item.get('quantity')
                    price = item.get('price')
                    
                    if not all([product_id, quantity, price]):
                        raise ValidationError("Invalid order item data")
                    
                    # Verify stock
                    stock = ProductService.get_stock(product_id)
                    if stock < quantity:
                        logger.warning(f"Insufficient stock for product {product_id}: needed {quantity}, available {stock}")
                        raise InsufficientStockError(product_id, quantity, stock)
                    
                    # Reduce stock (will be committed with transaction)
                    ProductService.reduce_stock(product_id, quantity)
                    
                    # Generate item ID
                    cursor.execute("SELECT ORDERS_SEQ.NEXTVAL FROM DUAL")
                    item_id = cursor.fetchone()[0]
                    
                    # Insert order item (omit CREATED_AT to support DBs without the column)
                    cursor.execute(
                        """
                        INSERT INTO ORDERS (ORDER_ID, ITEM_ID, PRODUCT_ID, QUANTITY, PRICE, STATUS, USER_ID)
                        VALUES (:order_id, :item_id, :product_id, :quantity, :price, :status, :user_id)
                        """,
                        {
                            "order_id": order_id,
                            "item_id": item_id,
                            "product_id": product_id,
                            "quantity": quantity,
                            "price": price,
                            "status": "PENDING",
                            "user_id": user_id,
                        }
                    )
                    
                    subtotal = price * quantity
                    total_amount += subtotal
                    
                    items_out.append({
                        "order_id": order_id,
                        "item_id": item_id,
                        "product_id": product_id,
                        "quantity": quantity,
                        "price": price,
                        "subtotal": subtotal
                    })
                
                logger.info(f"Order {order_id} created for user {user_id} with {len(items_out)} items, total: {total_amount}")
                
                return {
                    "order_id": order_id,
                    "user_id": user_id,
                    "total_amount": total_amount,
                    "status": "PENDING",
                    "items": items_out,
                    "message": "Order placed successfully"
                }
                
        except (InsufficientStockError, ValidationError):
            raise
        except Exception as e:
            logger.error(f"Order creation failed: {e}")
            raise DatabaseError(f"Order creation failed: {str(e)}")
    
    @staticmethod
    def get_order_by_id(order_id: int) -> Dict:
        """Get order details by ID"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                # Get order items
                cursor.execute(
                    """
                    SELECT ORDER_ID, ITEM_ID, PRODUCT_ID, QUANTITY, PRICE, STATUS, USER_ID
                    FROM ORDERS WHERE ORDER_ID = :id
                    """,
                    {"id": order_id}
                )
                
                rows = cursor.fetchall()
                
                if not rows:
                    raise ResourceNotFoundError("Order", order_id)
                
                # Build response
                first_row = rows[0]
                items = []
                total = 0

                for row in rows:
                    subtotal = row[3] * row[4]
                    total += subtotal

                    items.append({
                        "order_id": row[0],
                        "item_id": row[1],
                        "product_id": row[2],
                        "quantity": row[3],
                        "price": row[4],
                        "subtotal": subtotal
                    })

                return {
                    "order_id": first_row[0],
                    "user_id": first_row[6],
                    "total_amount": total,
                    "status": first_row[5],
                    "items": items,
                    "created_at": None
                }
        except ResourceNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Get order failed: {e}")
            raise DatabaseError("Get order failed")
    
    @staticmethod
    def get_orders_for_user(user_id: int, page: int = 1, page_size: int = 20) -> Dict:
        """Get user's orders"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                cursor.execute(
                    "SELECT COUNT(DISTINCT ORDER_ID) FROM ORDERS WHERE USER_ID = :b_uid",
                    {"b_uid": user_id}
                )
                total = cursor.fetchone()[0]
                
                start = (page - 1) * page_size + 1
                end = page * page_size

                # Use numeric literals for ROWNUM bounds to avoid bind issues
                sql = f"""
                    SELECT ORDER_ID, ITEM_ID, PRODUCT_ID, QUANTITY, PRICE, STATUS, USER_ID
                    FROM (
                        SELECT a.*, ROWNUM rnum FROM (
                            SELECT ORDER_ID, ITEM_ID, PRODUCT_ID, QUANTITY, PRICE, STATUS, USER_ID
                            FROM ORDERS WHERE USER_ID = :b_uid ORDER BY ORDER_ID DESC
                        ) a WHERE ROWNUM <= {end}
                    ) WHERE rnum >= {start}
                    """
                cursor.execute(sql, {"b_uid": user_id})
                
                items = []
                for row in cursor.fetchall():
                    items.append({
                        "order_id": row[0],
                        "item_id": row[1],
                        "product_id": row[2],
                        "quantity": row[3],
                        "price": row[4],
                        "status": row[5],
                        "created_at": None
                    })
                
                return {
                    "total": total,
                    "page": page,
                    "page_size": page_size,
                    "items": items
                }
        except Exception as e:
            logger.error(f"Get user orders failed: {e}")
            raise DatabaseError("Get user orders failed")
    
    @staticmethod
    def update_order_status(order_id: int, new_status: str) -> Dict:
        """Update order status"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                # Verify order exists
                cursor.execute(
                    "SELECT COUNT(*) FROM ORDERS WHERE ORDER_ID = :id",
                    {"id": order_id}
                )
                if cursor.fetchone()[0] == 0:
                    raise ResourceNotFoundError("Order", order_id)
                
                # Update all items in order
                cursor.execute(
                    "UPDATE ORDERS SET STATUS = :status WHERE ORDER_ID = :id",
                    {"status": new_status, "id": order_id}
                )
                
                logger.info(f"Order {order_id} status updated to {new_status}")
                return {"message": f"Order status updated to {new_status}"}
                
        except ResourceNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Update order status failed: {e}")
            raise DatabaseError("Update order status failed")
    
    @staticmethod
    def cancel_order(order_id: int) -> Dict:
        """
        Cancel order and restore inventory
        
        Args:
            order_id: Order ID to cancel
            
        Returns:
            Cancellation confirmation
            
        Raises:
            ValidationError: If order cannot be cancelled
            DatabaseError: If operation fails
        """
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                # Get order items to restore stock
                cursor.execute(
                    "SELECT PRODUCT_ID, QUANTITY FROM ORDERS WHERE ORDER_ID = :id",
                    {"id": order_id}
                )
                
                items = cursor.fetchall()
                if not items:
                    raise ResourceNotFoundError("Order", order_id)
                
                # Check if order can be cancelled (not shipped/delivered)
                cursor.execute(
                    "SELECT STATUS FROM ORDERS WHERE ORDER_ID = :id",
                    {"id": order_id}
                )
                status = cursor.fetchone()
                
                if status and status[0] in ['SHIPPED', 'DELIVERED', 'RETURNED']:
                    raise ValidationError(f"Cannot cancel order with status {status[0]}")
                
                # Restore stock for each item
                for item in items:
                    product_id = item[0]
                    quantity = item[1]
                    
                    cursor.execute(
                        "UPDATE PRODUCTS SET STOCK = STOCK + :qty WHERE PRODUCT_ID = :id",
                        {"qty": quantity, "id": product_id}
                    )
                
                # Update order status
                cursor.execute(
                    "UPDATE ORDERS SET STATUS = :status WHERE ORDER_ID = :id",
                    {"status": "CANCELLED", "id": order_id}
                )
                
                logger.info(f"Order {order_id} cancelled and inventory restored")
                return {"message": "Order cancelled successfully"}
                
        except (ResourceNotFoundError, ValidationError):
            raise
        except Exception as e:
            logger.error(f"Cancel order failed: {e}")
            raise DatabaseError("Cancel order failed")
    
    @staticmethod
    def get_all_orders(page: int = 1, page_size: int = 20) -> Dict:
        """Get all orders (admin only)"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT COUNT(DISTINCT ORDER_ID) FROM ORDERS")
                total = cursor.fetchone()[0]
                
                start = (page - 1) * page_size + 1
                end = page * page_size

                sql = f"""
                    SELECT ORDER_ID, ITEM_ID, PRODUCT_ID, QUANTITY, PRICE, STATUS, USER_ID
                    FROM (
                        SELECT a.*, ROWNUM rnum FROM (
                            SELECT ORDER_ID, ITEM_ID, PRODUCT_ID, QUANTITY, PRICE, STATUS, USER_ID
                            FROM ORDERS ORDER BY ORDER_ID DESC
                        ) a WHERE ROWNUM <= {end}
                    ) WHERE rnum >= {start}
                    """
                cursor.execute(sql)
                
                items = []
                for row in cursor.fetchall():
                    items.append({
                        "order_id": row[0],
                        "item_id": row[1],
                        "product_id": row[2],
                        "quantity": row[3],
                        "price": row[4],
                        "status": row[5],
                        "user_id": row[6],
                        "created_at": None
                    })
                
                return {
                    "total": total,
                    "page": page,
                    "page_size": page_size,
                    "items": items
                }
        except Exception as e:
            logger.error(f"Get all orders failed: {e}")
            raise DatabaseError("Get all orders failed")
