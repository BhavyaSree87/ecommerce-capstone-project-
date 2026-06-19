from app.database.db import get_connection

tables = ['USERS', 'PRODUCTS', 'CART', 'WISHLIST', 'ORDERS', 'PAYMENTS']
conn = get_connection()
cur = conn.cursor()
for table in tables:
    query = f"SELECT COLUMN_NAME, DATA_TYPE, NULLABLE FROM USER_TAB_COLUMNS WHERE TABLE_NAME = '{table}' ORDER BY COLUMN_ID"
    cur.execute(query)
    cols = cur.fetchall()
    print(f"\n{table} columns:")
    for col in cols:
        print(col)
cur.close()
conn.close()
