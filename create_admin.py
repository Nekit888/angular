from argon2 import PasswordHasher
import pymysql

ph = PasswordHasher()
password_hash = ph.hash("password")

print(f"Хеш пароля: {password_hash}")

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="root", 
    database="final_db",
    charset="utf8",
    autocommit=True
)

with conn.cursor() as cur:
    cur.execute("DELETE FROM admins WHERE admin_login = 'admin_test1'")
    cur.execute(
        "INSERT INTO admins (admin_login, admin_password_hash, is_active_admin, admin_birth_date, created_at) "
        "VALUES (%s, %s, %s, %s, NOW())",
        ("admin_test1", password_hash, 1, "2000-01-01")
    )
    print("✅ Админ создан!")

conn.close()