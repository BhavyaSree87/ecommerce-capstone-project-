from fastapi import APIRouter, Depends, HTTPException, Query
from app.database.db import get_connection
from app.schemas.payment_schema import PaymentCreate, PaymentOut, PaginatedPayments
from app.utils.auth_dependency import current_user, admin_only

router = APIRouter()


@router.post("/pay", response_model=PaymentOut)
def make_payment(payment: PaymentCreate, user=Depends(current_user)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT PAYMENTS_SEQ.NEXTVAL FROM DUAL")
        pid = cursor.fetchone()[0]
        
        if getattr(payment, 'transaction_id', None):
            cursor.execute(
                """
                INSERT INTO PAYMENTS (PAYMENT_ID, ORDER_ID, PAYMENT_METHOD, PAYMENT_STATUS, AMOUNT, TRANSACTION_ID)
                VALUES (:pid, :order_id, :payment_method, :payment_status, :amount, :transaction_id)
                """,
                {
                    "pid": pid,
                    "order_id": payment.order_id,
                    "payment_method": payment.payment_method,
                    "payment_status": payment.payment_status,
                    "amount": payment.amount,
                    "transaction_id": payment.transaction_id,
                },
            )
        else:
            cursor.execute(
                """
                INSERT INTO PAYMENTS (PAYMENT_ID, ORDER_ID, PAYMENT_METHOD, PAYMENT_STATUS, AMOUNT)
                VALUES (:pid, :order_id, :payment_method, :payment_status, :amount)
                """,
                {"pid": pid, "order_id": payment.order_id, "payment_method": payment.payment_method, "payment_status": payment.payment_status, "amount": payment.amount},
            )
        conn.commit()
        return {"payment_id": pid, "order_id": payment.order_id, "payment_method": payment.payment_method, "payment_status": payment.payment_status, "amount": payment.amount}
    finally:
        cursor.close()
        conn.close()


@router.get("/all", dependencies=[Depends(admin_only)])
def get_payments(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
                cursor.execute("SELECT COUNT(*) FROM PAYMENTS")
                total = cursor.fetchone()[0]
                start = (page - 1) * page_size + 1
                end = page * page_size
                sql = f"""
                        SELECT * FROM (
                            SELECT a.*, ROWNUM rnum FROM (
                                SELECT PAYMENT_ID, ORDER_ID, PAYMENT_METHOD, PAYMENT_STATUS, AMOUNT FROM PAYMENTS ORDER BY PAYMENT_ID DESC
                            ) a WHERE ROWNUM <= {end}
                        ) WHERE rnum >= {start}
                        """
                cursor.execute(sql)
                rows = cursor.fetchall()
                return {"total": total, "page": page, "page_size": page_size, "items": rows}
    finally:
        cursor.close()
        conn.close()


@router.get("/order/{order_id}")
def get_payment(order_id: int, user=Depends(current_user)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT PAYMENT_ID, ORDER_ID, PAYMENT_METHOD, PAYMENT_STATUS, AMOUNT FROM PAYMENTS WHERE ORDER_ID = :id", {"id": order_id})
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Payment not found")
        return {"payment_id": row[0], "order_id": row[1], "payment_method": row[2], "payment_status": row[3], "amount": row[4]}
    finally:
        cursor.close()
        conn.close()


@router.get("/user/{user_id}")
def get_payments_for_user(user_id: int, page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), user=Depends(current_user)):
    if user.get("role") != "ADMIN" and user.get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    conn = get_connection()
    cursor = conn.cursor()
    try:
                
                cursor.execute("SELECT COUNT(*) FROM PAYMENTS p JOIN ORDERS o ON p.ORDER_ID = o.ORDER_ID WHERE o.USER_ID = :user_id", {"user_id": user_id})
                total = cursor.fetchone()[0]
                start = (page - 1) * page_size + 1
                end = page * page_size
                sql = f"""
                        SELECT * FROM (
                            SELECT a.*, ROWNUM rnum FROM (
                                SELECT p.PAYMENT_ID, p.ORDER_ID, p.PAYMENT_METHOD, p.PAYMENT_STATUS, p.AMOUNT FROM PAYMENTS p JOIN ORDERS o ON p.ORDER_ID = o.ORDER_ID WHERE o.USER_ID = :user_id ORDER BY p.PAYMENT_ID DESC
                            ) a WHERE ROWNUM <= {end}
                        ) WHERE rnum >= {start}
                        """
                cursor.execute(sql, {"user_id": user_id})
                rows = cursor.fetchall()
                return {"total": total, "page": page, "page_size": page_size, "items": rows}
    finally:
        cursor.close()
        conn.close()


@router.put("/status/{payment_id}", dependencies=[Depends(admin_only)])
def update_payment_status(payment_id: int, status: str):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE PAYMENTS SET PAYMENT_STATUS = :status WHERE PAYMENT_ID = :id", {"status": status, "id": payment_id})
        conn.commit()
        return {"message": "Payment Status Updated"}
    finally:
        cursor.close()
        conn.close()