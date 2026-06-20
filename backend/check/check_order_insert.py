from app.database.db import get_connection

conn = get_connection()
cur = conn.cursor()
try:
    cur.execute("SELECT COLUMN_NAME FROM USER_TAB_COLUMNS WHERE TABLE_NAME='ORDERS' ORDER BY COLUMN_ID")
    print('ORDERS columns:', [r[0] for r in cur.fetchall()])

    # Verify simple select can see USER_ID and ORDER_ID
    try:
        cur.execute("SELECT ORDER_ID, ITEM_ID, PRODUCT_ID, QUANTITY, PRICE, STATUS, USER_ID FROM ORDERS WHERE ROWNUM = 1")
        row = cur.fetchone()
        print('Select sample row:', row)
    except Exception as e:
        print('Select failed:', type(e).__name__, e)

    # Try a dummy insert with rollback
    try:
        cur.execute("INSERT INTO ORDERS (ORDER_ID, ITEM_ID, PRODUCT_ID, QUANTITY, PRICE, STATUS, USER_ID) VALUES (1000000, 1000000, 1, 1, 1, 'PENDING', 1)")
        print('Insert executed successfully')
        conn.rollback()
    except Exception as e:
        print('Insert failed:', type(e).__name__, e)

except Exception as e:
    print('Error:', type(e).__name__, e)
finally:
    cur.close()
    conn.close()
