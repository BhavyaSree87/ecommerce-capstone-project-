from app.database.db import get_connection
conn = get_connection()
cur = conn.cursor()
try:
    cur.execute("SELECT COUNT(*) FROM USERS")
    print('users_count', cur.fetchone()[0])
    cur.execute("SELECT SEQUENCE_NAME FROM USER_SEQUENCES WHERE SEQUENCE_NAME='USER_SEQ'")
    print('USER_SEQ exists', cur.fetchone())
    cur.execute("SELECT SEQUENCE_NAME FROM USER_SEQUENCES WHERE SEQUENCE_NAME='PRODUCT_SEQ'")
    print('PRODUCT_SEQ exists', cur.fetchone())
finally:
    cur.close()
    conn.close()
