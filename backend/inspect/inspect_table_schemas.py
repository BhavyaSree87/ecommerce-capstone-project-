from app.database.db import get_connection

tables = ['ORDERS', 'PAYMENTS', 'USERS', 'CART', 'WISHLIST', 'PRODUCTS']
conn = get_connection()
cur = conn.cursor()
for table in tables:
    cur.execute("SELECT COLUMN_NAME FROM USER_TAB_COLUMNS WHERE TABLE_NAME = :table ORDER BY COLUMN_ID", {'table': table})
    cols = [row[0] for row in cur.fetchall()]
    print(table, cols)
cur.close()
conn.close()
