import pymysql

def get_conn():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="дашкевич",
        charset="utf8mb4",
        autocommit=True
    )

def get_all_roles():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM roles")
    res = cur.fetchall()
    cur.close()
    conn.close()
    return res

def get_role_by_id(id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM roles WHERE role_id = %s", (id,))
    res = cur.fetchone()
    cur.close()
    conn.close()
    return res

def create_role(name, desc, active):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO roles (role_name, role_description, is_active) VALUES (%s, %s, %s)", (name, desc, active))
    id = cur.lastrowid
    cur.close()
    conn.close()
    return (id, name, desc, active)

def update_role(id, name, desc, active):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE roles SET role_name=%s, role_description=%s, is_active=%s WHERE role_id=%s", (name, desc, active, id))
    cur.close()
    conn.close()

def delete_role(id, hard):
    conn = get_conn()
    cur = conn.cursor()
    if hard:
        cur.execute("DELETE FROM roles WHERE role_id=%s", (id,))
    else:
        cur.execute("UPDATE roles SET is_active=0 WHERE role_id=%s", (id,))
    cur.close()
    conn.close()