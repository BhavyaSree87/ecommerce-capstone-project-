from app.database.db import get_connection

conn = get_connection()
cur = conn.cursor()
cur.execute("SELECT COLUMN_NAME FROM USER_TAB_COLUMNS WHERE TABLE_NAME='ORDERS' ORDER BY COLUMN_ID")
cols = cur.fetchall()
print('ORDERS columns:', cols)
cur.close()
conn.close()
