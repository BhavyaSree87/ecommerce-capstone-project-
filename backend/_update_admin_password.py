from app.database.db import get_connection
from app.utils.password import hash_password

email = 'admin_jwt_test@example.com'
new_password = 'Admin@123'
new_hash = hash_password(new_password)
print('Generated bcrypt hash:')
print(new_hash)

sql = 'UPDATE USERS SET PASSWORD = :pwd WHERE EMAIL = :email AND ROLE = :role'
print('\nExact SQL to run:')
print(sql)
print('With parameters:')
print({'pwd': new_hash, 'email': email, 'role': 'ADMIN'})

conn = get_connection()
cursor = conn.cursor()
try:
    cursor.execute(sql, {'pwd': new_hash, 'email': email, 'role': 'ADMIN'})
    rows = cursor.rowcount
    conn.commit()
    print(f'Rows updated: {rows}')
    if rows == 0:
        print(f'No ADMIN user found with email {email}')
finally:
    cursor.close()
    conn.close()
