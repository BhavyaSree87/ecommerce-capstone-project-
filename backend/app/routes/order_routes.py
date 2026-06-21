from fastapi import APIRouter, HTTPException, Depends, Query
from app.database.db import get_connection
from app.schemas.order_schema import OrderPlace, OrderPlacedResponse, OrderStatusUpdate, OrderHistoryResponse
from app.utils.auth_dependency import current_user, admin_only
from app.logger import get_logger
from typing import List
from datetime import datetime

logger = get_logger("order_routes")
router = APIRouter()


def _get_inventory_for_update(cursor, product_id: int):
    cursor.execute(
        """
        SELECT AVAILABLE_STOCK, RESERVED_STOCK
        FROM INVENTORY
        WHERE PRODUCT_ID = :id
        FOR UPDATE
        """,
        {"id": product_id},
    )
    return cursor.fetchone()


@router.post("/create", response_model=OrderPlacedResponse)
def create_order(order: OrderPlace, user=Depends(current_user)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        
        cursor.execute("SELECT ORDERS_SEQ.NEXTVAL FROM DUAL")
        order_id = cursor.fetchone()[0]

        items_out = []
        total_calc = 0

        for it in order.items:
            cursor.execute("SELECT STOCK FROM PRODUCTS WHERE PRODUCT_ID = :id FOR UPDATE", {"id": it.product_id})
            row = cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail=f"Product {it.product_id} not found")

            stock = row[0]
            inventory_row = _get_inventory_for_update(cursor, it.product_id)
            if not inventory_row:
                # Auto-create inventory record for existing product using current STOCK value
                try:
                    cursor.execute(
                        "INSERT INTO INVENTORY (INVENTORY_ID, PRODUCT_ID, AVAILABLE_STOCK, RESERVED_STOCK, LAST_UPDATED) VALUES (INVENTORY_SEQ.NEXTVAL, :pid, :stk, 0, SYSDATE)",
                        {"pid": it.product_id, "stk": stock},
                    )
                    # re-fetch the inventory row under lock
                    inventory_row = _get_inventory_for_update(cursor, it.product_id)
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Failed to create inventory for product {it.product_id}: {e}")

            available_stock, reserved_stock = inventory_row
            if available_stock < it.quantity:
                raise HTTPException(status_code=400, detail=f"Insufficient inventory for product {it.product_id}")
            if stock < it.quantity:
                raise HTTPException(status_code=400, detail=f"Insufficient stock for product {it.product_id}")

            cursor.execute(
                "UPDATE PRODUCTS SET STOCK = STOCK - :q WHERE PRODUCT_ID = :id",
                {"q": it.quantity, "id": it.product_id},
            )
            cursor.execute(
                """
                UPDATE INVENTORY
                SET AVAILABLE_STOCK = AVAILABLE_STOCK - :q,
                    RESERVED_STOCK = RESERVED_STOCK + :q,
                    LAST_UPDATED = SYSDATE
                WHERE PRODUCT_ID = :id
                """,
                {"q": it.quantity, "id": it.product_id},
            )

            cursor.execute("SELECT ORDERS_SEQ.NEXTVAL FROM DUAL")
            item_id = cursor.fetchone()[0]

            cursor.execute(
                """
                INSERT INTO ORDERS (ORDER_ID, ITEM_ID, PRODUCT_ID, QUANTITY, PRICE, STATUS, USER_ID)
                VALUES (:order_id, :item_id, :product_id, :quantity, :price, :status, :user_id)
                """,
                {
                    "order_id": order_id,
                    "item_id": item_id,
                    "product_id": it.product_id,
                    "quantity": it.quantity,
                    "price": it.price,
                    "status": "Order Placed",
                    "user_id": user.get("user_id"),
                },
            )

            items_out.append({
                "order_id": order_id,
                "item_id": item_id,
                "product_id": it.product_id,
                "quantity": it.quantity,
                "price": it.price,
                "subtotal": it.price * it.quantity,
                "status": "Order Placed",
            })
            total_calc += it.price * it.quantity

        conn.commit()
        logger.info(f"Order {order_id} created for user {user.get('user_id')} with {len(items_out)} items")

        return {
            "order_id": order_id,
            "user_id": user.get("user_id"),
            "total_amount": total_calc,
            "status": "Order Placed",
            "items": items_out,
        }
    except HTTPException:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        logger.error(f"Order creation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.get("/all", dependencies=[Depends(admin_only)])
def get_orders(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        try:
            cursor.execute("SELECT COUNT(*) FROM ORDERS")
            total = cursor.fetchone()[0]
            start = (page - 1) * page_size + 1
            end = page * page_size
            sql = f"""
                SELECT * FROM (
                    SELECT a.*, ROWNUM rnum FROM (
                        SELECT ORDER_ID, ITEM_ID, PRODUCT_ID, QUANTITY, PRICE, STATUS, USER_ID, CREATED_AT FROM ORDERS ORDER BY CREATED_AT DESC
                    ) a WHERE ROWNUM <= {end}
                ) WHERE rnum >= {start}
                """
            cursor.execute(sql)
            rows = cursor.fetchall()
            return {
                "total": total,
                "page": page,
                "page_size": page_size,
                "items": [
                    {
                        "id": row[0],
                        "item_id": row[1],
                        "product_id": row[2],
                        "quantity": row[3],
                        "price": row[4],
                        "status": row[5],
                        "user_id": row[6],
                        "created_at": row[7],
                        "total_amount": row[3] * row[4],
                    }
                    for row in rows
                ],
            }
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.get("/{order_id}", dependencies=[Depends(admin_only)])
def get_order(order_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT ORDER_ID, ITEM_ID, PRODUCT_ID, QUANTITY, PRICE, STATUS, USER_ID, CREATED_AT FROM ORDERS WHERE ORDER_ID = :id",
            {"id": order_id},
        )
        rows = cursor.fetchall()
        if not rows:
            raise HTTPException(status_code=404, detail="Order not found")

        items = [
            {
                "order_id": row[0],
                "item_id": row[1],
                "product_id": row[2],
                "quantity": row[3],
                "price": row[4],
                "status": row[5],
                "user_id": row[6],
                "created_at": row[7],
                "total_amount": row[3] * row[4],
            }
            for row in rows
        ]

        return {
            "order_id": order_id,
            "items": items,
            "user_id": items[0]["user_id"],
            "status": items[-1]["status"],
            "created_at": items[0]["created_at"],
            "total_amount": sum(item["total_amount"] for item in items),
        }
    finally:
        cursor.close()
        conn.close()


@router.get("/user/{user_id}")
def get_orders_for_user(user_id: int, page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), user=Depends(current_user)):
    
    if user.get("role") != "ADMIN" and user.get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    conn = get_connection()
    cursor = conn.cursor()
    try:
        try:
            cursor.execute("SELECT COUNT(*) FROM ORDERS WHERE USER_ID = :b_uid", {"b_uid": user_id})
            total = cursor.fetchone()[0]
            start = (page - 1) * page_size + 1
            end = page * page_size
            sql = f"""
                SELECT * FROM (
                    SELECT a.*, ROWNUM rnum FROM (
                        SELECT ORDER_ID, ITEM_ID, PRODUCT_ID, QUANTITY, PRICE, STATUS, USER_ID, CREATED_AT FROM ORDERS WHERE USER_ID = :b_uid ORDER BY CREATED_AT DESC
                    ) a WHERE ROWNUM <= {end}
                ) WHERE rnum >= {start}
                """
            cursor.execute(sql, {"b_uid": user_id})
            rows = cursor.fetchall()
            return {"total": total, "page": page, "page_size": page_size, "items": rows}
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.put("/status/{order_id}")
def update_order_status(order_id: int, payload: OrderStatusUpdate, user=Depends(admin_only)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT DISTINCT STATUS FROM ORDERS WHERE ORDER_ID = :id", {"id": order_id})
        current_status_row = cursor.fetchone()
        if not current_status_row:
            raise HTTPException(status_code=404, detail="Order not found")

        current_status = current_status_row[0]
        new_status = payload.status

        if current_status == new_status:
            return {"message": "Order Status Updated"}

        if new_status == "CANCELLED":
            cursor.execute(
                "SELECT PRODUCT_ID, QUANTITY FROM ORDERS WHERE ORDER_ID = :id",
                {"id": order_id},
            )
            order_items = cursor.fetchall()
            if not order_items:
                raise HTTPException(status_code=404, detail="Order details not found")

            for product_id, quantity in order_items:
                cursor.execute(
                    "UPDATE PRODUCTS SET STOCK = STOCK + :qty WHERE PRODUCT_ID = :id",
                    {"qty": quantity, "id": product_id},
                )

                inventory_row = _get_inventory_for_update(cursor, product_id)
                if not inventory_row:
                    raise HTTPException(status_code=400, detail=f"Inventory record not found for product {product_id}")

                _, reserved_stock = inventory_row
                if reserved_stock < quantity:
                    raise HTTPException(status_code=400, detail=f"Reserved inventory insufficient for product {product_id}")

                cursor.execute(
                    """
                    UPDATE INVENTORY
                    SET AVAILABLE_STOCK = AVAILABLE_STOCK + :qty,
                        RESERVED_STOCK = RESERVED_STOCK - :qty,
                        LAST_UPDATED = SYSDATE
                    WHERE PRODUCT_ID = :id
                    """,
                    {"qty": quantity, "id": product_id},
                )
        elif new_status == "DELIVERED":
            cursor.execute(
                "SELECT PRODUCT_ID, QUANTITY FROM ORDERS WHERE ORDER_ID = :id",
                {"id": order_id},
            )
            order_items = cursor.fetchall()
            if not order_items:
                raise HTTPException(status_code=404, detail="Order details not found")

            for product_id, quantity in order_items:
                inventory_row = _get_inventory_for_update(cursor, product_id)
                if not inventory_row:
                    raise HTTPException(status_code=400, detail=f"Inventory record not found for product {product_id}")

                _, reserved_stock = inventory_row
                if reserved_stock < quantity:
                    raise HTTPException(status_code=400, detail=f"Reserved inventory insufficient for product {product_id}")

                cursor.execute(
                    """
                    UPDATE INVENTORY
                    SET RESERVED_STOCK = RESERVED_STOCK - :qty,
                        LAST_UPDATED = SYSDATE
                    WHERE PRODUCT_ID = :id
                    """,
                    {"qty": quantity, "id": product_id},
                )

        cursor.execute("UPDATE ORDERS SET STATUS = :status WHERE ORDER_ID = :id", {"status": new_status, "id": order_id})
        conn.commit()
        logger.info(f"Order {order_id} status changed from {current_status} to {new_status}")
        return {"message": "Order Status Updated"}
    except HTTPException:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        logger.error(f"Order status update failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()