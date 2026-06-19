from app.database.db import get_connection
import oracledb

conn = get_connection()
cur = conn.cursor()

try:
    cur.execute("SELECT COLUMN_NAME FROM USER_TAB_COLUMNS WHERE TABLE_NAME='ORDERS' ORDER BY COLUMN_ID")
    existing = {row[0] for row in cur.fetchall()}
    print('Existing ORDERS columns:', existing)

    if 'USER_ID' not in existing:
        print('Adding USER_ID column')
        cur.execute('ALTER TABLE ORDERS ADD (USER_ID NUMBER)')
        try:
            cur.execute('ALTER TABLE ORDERS ADD CONSTRAINT FK_ORDERS_USER FOREIGN KEY (USER_ID) REFERENCES USERS(ID)')
        except oracledb.DatabaseError as e:
            print('Could not add FK_ORDERS_USER:', e)

    if 'CREATED_AT' not in existing:
        print('Adding CREATED_AT column')
        cur.execute("ALTER TABLE ORDERS ADD (CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

    conn.commit()
    print('Schema fix complete')
except Exception as e:
    conn.rollback()
    print('Schema fix failed:', e)
finally:
    cur.close()
    conn.close()
