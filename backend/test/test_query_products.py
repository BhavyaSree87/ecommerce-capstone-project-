from app.database.db import get_connection

conn = get_connection()
cur = conn.cursor()
start = 1
end = 10
try:
    cur.execute("SELECT COUNT(*) FROM PRODUCTS")
    print('count', cur.fetchone()[0])
    cur.execute('''
        SELECT * FROM (
          SELECT a.*, ROWNUM rnum FROM (
            SELECT PRODUCT_ID, PRODUCT_NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, STOCK, IMAGE_URL, RATING FROM PRODUCTS ORDER BY PRODUCT_ID DESC
          ) a WHERE ROWNUM <= :end_
        ) WHERE rnum >= :start
    ''', {"start": start, "end_": end})
    rows = cur.fetchall()
    print('rows', rows)
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    cur.close()
    conn.close()
