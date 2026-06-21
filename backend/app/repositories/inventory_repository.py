from datetime import datetime


def get_inventory_by_product_id(cursor, product_id: int):
    cursor.execute(
        """
        SELECT INVENTORY_ID, PRODUCT_ID, AVAILABLE_STOCK, RESERVED_STOCK, LAST_UPDATED
        FROM INVENTORY
        WHERE PRODUCT_ID = :product_id
        """,
        {"product_id": product_id}
    )
    return cursor.fetchone()


def create_inventory(cursor, product_id: int, available_stock: int, reserved_stock: int = 0, last_updated: datetime = None):
    """Insert an inventory record for a product. Uses INVENTORY_SEQ for INVENTORY_ID and SYSDATE for LAST_UPDATED."""
    # Oracle SYSDATE is used for LAST_UPDATED to avoid binding datetime conversions
    sql = """
    INSERT INTO INVENTORY (INVENTORY_ID, PRODUCT_ID, AVAILABLE_STOCK, RESERVED_STOCK, LAST_UPDATED)
    VALUES (INVENTORY_SEQ.NEXTVAL, :product_id, :available_stock, :reserved_stock, SYSDATE)
    """
    params = {
        "product_id": product_id,
        "available_stock": available_stock,
        "reserved_stock": reserved_stock,
    }
    cursor.execute(sql, params)


def update_inventory(cursor, product_id: int, available_stock: int = None, reserved_stock: int = None, last_updated: datetime = None):
    fields = []
    params = {"product_id": product_id}

    if available_stock is not None:
        fields.append("AVAILABLE_STOCK = :available_stock")
        params["available_stock"] = available_stock

    if reserved_stock is not None:
        fields.append("RESERVED_STOCK = :reserved_stock")
        params["reserved_stock"] = reserved_stock

    if last_updated is None:
        last_updated = datetime.utcnow()
    fields.append("LAST_UPDATED = :last_updated")
    params["last_updated"] = last_updated

    if not fields:
        return 0

    sql = f"UPDATE INVENTORY SET {', '.join(fields)} WHERE PRODUCT_ID = :product_id"
    cursor.execute(sql, params)
    return cursor.rowcount


def count_inventory(cursor):
    cursor.execute("SELECT COUNT(*) FROM INVENTORY")
    return cursor.fetchone()[0]


def list_inventory(cursor, page: int, page_size: int):
    start = (page - 1) * page_size + 1
    end = page * page_size
    cursor.execute(
        f"""
        SELECT * FROM (
            SELECT a.*, ROWNUM rnum FROM (
                SELECT INVENTORY_ID, PRODUCT_ID, AVAILABLE_STOCK, RESERVED_STOCK, LAST_UPDATED
                FROM INVENTORY ORDER BY INVENTORY_ID DESC
            ) a WHERE ROWNUM <= {end}
        ) WHERE rnum >= {start}
        """
    )
    return cursor.fetchall()


def count_low_stock(cursor):
    cursor.execute("SELECT COUNT(*) FROM INVENTORY WHERE AVAILABLE_STOCK < 10")
    return cursor.fetchone()[0]


def list_low_stock(cursor, page: int, page_size: int):
    start = (page - 1) * page_size + 1
    end = page * page_size
    cursor.execute(
        f"""
        SELECT * FROM (
            SELECT a.*, ROWNUM rnum FROM (
                SELECT INVENTORY_ID, PRODUCT_ID, AVAILABLE_STOCK, RESERVED_STOCK, LAST_UPDATED
                FROM INVENTORY WHERE AVAILABLE_STOCK < 10 ORDER BY AVAILABLE_STOCK ASC, INVENTORY_ID DESC
            ) a WHERE ROWNUM <= {end}
        ) WHERE rnum >= {start}
        """
    )
    return cursor.fetchall()
