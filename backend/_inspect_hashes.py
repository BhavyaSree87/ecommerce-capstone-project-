from app.database.db import get_connection

conn = get_connection()
cur = conn.cursor()
try:
    cur.execute("SELECT EMAIL, PASSWORD FROM USERS WHERE ROWNUM <= 5")
    rows = cur.fetchall()
    for email, pwd in rows:
        print(email, pwd[:50], '...' if len(pwd) > 50 else '')
finally:
    cur.close()
    conn.close()
