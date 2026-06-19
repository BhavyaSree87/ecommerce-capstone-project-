"""Payment service - handles payment operations"""

from app.database.db import get_db_context
from app.exceptions import ResourceNotFoundError, DatabaseError
from app.logger import get_logger
import oracledb
from typing import Dict

logger = get_logger("payment_service")


class PaymentService:
    """Service class for payment operations"""
    
    @staticmethod
    def create_payment(order_id: int, payment_data: Dict) -> Dict:
        """Create a payment record"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT PAYMENTS_SEQ.NEXTVAL FROM DUAL")
                payment_id = cursor.fetchone()[0]
                
                # Try insert including TRANSACTION_ID if provided; if DB doesn't have the column, retry without it
                try:
                    if payment_data.get('transaction_id') is not None:
                        cursor.execute(
                            """
                            INSERT INTO PAYMENTS (PAYMENT_ID, ORDER_ID, PAYMENT_METHOD, PAYMENT_STATUS, AMOUNT, TRANSACTION_ID)
                            VALUES (:pid, :order_id, :payment_method, :payment_status, :amount, :transaction_id)
                            """,
                            {
                                "pid": payment_id,
                                "order_id": order_id,
                                "payment_method": payment_data.get('payment_method'),
                                "payment_status": payment_data.get('payment_status', 'PENDING'),
                                "amount": payment_data.get('amount'),
                                "transaction_id": payment_data.get('transaction_id')
                            }
                        )
                    else:
                        # no transaction id supplied, insert minimal columns
                        cursor.execute(
                            """
                            INSERT INTO PAYMENTS (PAYMENT_ID, ORDER_ID, PAYMENT_METHOD, PAYMENT_STATUS, AMOUNT)
                            VALUES (:pid, :order_id, :payment_method, :payment_status, :amount)
                            """,
                            {
                                "pid": payment_id,
                                "order_id": order_id,
                                "payment_method": payment_data.get('payment_method'),
                                "payment_status": payment_data.get('payment_status', 'PENDING'),
                                "amount": payment_data.get('amount')
                            }
                        )
                except oracledb.DatabaseError as db_e:
                    # If TRANSACTION_ID isn't a valid column, retry without it
                    msg = str(db_e)
                    logger.warning(f"Create payment insert failed, retrying without TRANSACTION_ID: {msg}")
                    cursor.execute(
                        """
                        INSERT INTO PAYMENTS (PAYMENT_ID, ORDER_ID, PAYMENT_METHOD, PAYMENT_STATUS, AMOUNT)
                        VALUES (:pid, :order_id, :payment_method, :payment_status, :amount)
                        """,
                        {
                            "pid": payment_id,
                            "order_id": order_id,
                            "payment_method": payment_data.get('payment_method'),
                            "payment_status": payment_data.get('payment_status', 'PENDING'),
                            "amount": payment_data.get('amount')
                        }
                    )
                logger.info(f"Payment {payment_id} created for order {order_id}")
                
                return {
                    "payment_id": payment_id,
                    "order_id": order_id,
                    "payment_method": payment_data.get('payment_method'),
                    "payment_status": payment_data.get('payment_status', 'PENDING'),
                    "amount": payment_data.get('amount')
                }
        except Exception as e:
            logger.error(f"Create payment failed: {e}")
            raise DatabaseError("Payment creation failed")
    
    @staticmethod
    def get_payment_for_order(order_id: int) -> Dict:
        """Get payment for an order"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                cursor.execute(
                    """
                    SELECT PAYMENT_ID, ORDER_ID, PAYMENT_METHOD, PAYMENT_STATUS, AMOUNT
                    FROM PAYMENTS WHERE ORDER_ID = :id
                    """,
                    {"id": order_id}
                )
                
                row = cursor.fetchone()
                if not row:
                    raise ResourceNotFoundError("Payment", order_id)
                
                return {
                    "payment_id": row[0],
                    "order_id": row[1],
                    "payment_method": row[2],
                    "payment_status": row[3],
                    "amount": row[4]
                }
        except ResourceNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Get payment failed: {e}")
            raise DatabaseError("Get payment failed")
    
    @staticmethod
    def update_payment_status(payment_id: int, new_status: str) -> Dict:
        """Update payment status"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                cursor.execute(
                    "UPDATE PAYMENTS SET PAYMENT_STATUS = :status WHERE PAYMENT_ID = :id",
                    {"status": new_status, "id": payment_id}
                )
                
                if cursor.rowcount == 0:
                    raise ResourceNotFoundError("Payment", payment_id)
                
                logger.info(f"Payment {payment_id} status updated to {new_status}")
                return {"message": f"Payment status updated to {new_status}"}
                
        except ResourceNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Update payment status failed: {e}")
            raise DatabaseError("Update payment status failed")
    
    @staticmethod
    def get_payments_for_user(user_id: int, page: int = 1, page_size: int = 20) -> Dict:
        """Get payments for a user"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                cursor.execute(
                    "SELECT COUNT(*) FROM PAYMENTS p JOIN ORDERS o ON p.ORDER_ID = o.ORDER_ID WHERE o.USER_ID = :uid",
                    {"uid": user_id}
                )
                total = cursor.fetchone()[0]
                
                start = (page - 1) * page_size + 1
                end = page * page_size
                
                cursor.execute(
                    """
                    SELECT * FROM (
                      SELECT a.*, ROWNUM rnum FROM (
                        SELECT p.PAYMENT_ID, p.ORDER_ID, p.PAYMENT_METHOD, p.PAYMENT_STATUS, p.AMOUNT
                        FROM PAYMENTS p JOIN ORDERS o ON p.ORDER_ID = o.ORDER_ID
                        WHERE o.USER_ID = :uid ORDER BY p.PAYMENT_ID DESC
                      ) a WHERE ROWNUM <= :end
                    ) WHERE rnum >= :start
                    """,
                    {"uid": user_id, "start": start, "end": end}
                )
                
                items = []
                for row in cursor.fetchall():
                    items.append({
                        "payment_id": row[0],
                        "order_id": row[1],
                        "payment_method": row[2],
                        "payment_status": row[3],
                        "amount": row[4]
                    })
                
                return {
                    "total": total,
                    "page": page,
                    "page_size": page_size,
                    "items": items
                }
        except Exception as e:
            logger.error(f"Get user payments failed: {e}")
            raise DatabaseError("Get user payments failed")
    
    @staticmethod
    def get_all_payments(page: int = 1, page_size: int = 20) -> Dict:
        """Get all payments (admin)"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT COUNT(*) FROM PAYMENTS")
                total = cursor.fetchone()[0]
                
                start = (page - 1) * page_size + 1
                end = page * page_size
                
                cursor.execute(
                    """
                    SELECT * FROM (
                      SELECT a.*, ROWNUM rnum FROM (
                        SELECT PAYMENT_ID, ORDER_ID, PAYMENT_METHOD, PAYMENT_STATUS, AMOUNT
                        FROM PAYMENTS ORDER BY PAYMENT_ID DESC
                      ) a WHERE ROWNUM <= :end
                    ) WHERE rnum >= :start
                    """,
                    {"start": start, "end": end}
                )
                
                items = []
                for row in cursor.fetchall():
                    items.append({
                        "payment_id": row[0],
                        "order_id": row[1],
                        "payment_method": row[2],
                        "payment_status": row[3],
                        "amount": row[4]
                    })
                
                return {
                    "total": total,
                    "page": page,
                    "page_size": page_size,
                    "items": items
                }
        except Exception as e:
            logger.error(f"Get all payments failed: {e}")
            raise DatabaseError("Get all payments failed")
