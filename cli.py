import click
import pymysql
from argon2 import PasswordHasher
from application.admin_crud_service import get_admin_by_id, create_admin, update_admin, delete_admin
from application.roles.admin_role_service import get_all_roles, get_role_by_id, create_role, update_role, delete_role

ph = PasswordHasher()
current_user = None

def login():
    global current_user
    click.echo("\n=== ВХОД ===")
    login = click.prompt('Логин') #admin_test1
    password = click.prompt('Пароль') #password
    
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="final_db",
        charset="utf8mb4"
    )
    cur = conn.cursor()
    cur.execute("SELECT admin_login, admin_password_hash FROM admins WHERE admin_login = %s", (login,))
    admin = cur.fetchone()
    conn.close()
    
    if admin:
        try:
            ph.verify(admin[1], password)
            current_user = admin[0]
            click.echo(f"\nПривет, {current_user}!\n")
            return True
        except:
            click.echo("Пароль неверный\n")
            return False
    else:
        click.echo("Пользователь не найден\n")
        return False

# Функции админов
def get_admin():
    id = click.prompt('ID админа', type=int)
    click.echo(get_admin_by_id(id))

def create_adm():
    login = click.prompt('Логин')
    pwd = click.prompt('Пароль')
    active = click.prompt('Активен', type=bool)
    res = create_admin({"admin_login": login, "admin_password": pwd, "is_active_admin": active})
    click.echo(res)

def update_adm():
    id = click.prompt('ID админа', type=int)
    login = click.prompt('Логин')
    pwd = click.prompt('Пароль')
    active = click.prompt('Активен', type=bool)
    res = update_admin(id, {"admin_login": login, "admin_password": pwd, "is_active_admin": active})
    click.echo(res)

def delete_adm():
    id = click.prompt('ID админа', type=int)
    delete_admin(id, hard=True)
    click.echo("Удален")

# Функции ролей
def all_roles():
    for r in get_all_roles():
        click.echo(r)

def role_by_id():
    id = click.prompt('ID роли', type=int)
    click.echo(get_role_by_id(id))

def create_r():
    name = click.prompt('Название')
    desc = click.prompt('Описание')
    active = click.prompt('Активна (1/0)', type=int)
    click.echo(create_role(name, desc, active))

def update_r():
    id = click.prompt('ID роли', type=int)
    name = click.prompt('Название')
    desc = click.prompt('Описание')
    active = click.prompt('Активна (1/0)', type=int)
    update_role(id, name, desc, active)
    click.echo("Обновлено")

def delete_r():
    id = click.prompt('ID роли', type=int)
    hard = click.prompt('Полное удаление', type=bool)
    delete_role(id, hard)
    click.echo("Удалено")

def admin_menu():
    while True:
        choice = click.prompt("""
1. Получить админа
2. Создать админа
3. Обновить админа
4. Удалить админа
5. Назад
""", type=int)
        if choice == 1: get_admin()
        elif choice == 2: create_adm()
        elif choice == 3: update_adm()
        elif choice == 4: delete_adm()
        elif choice == 5: break
        else: click.echo("1-5")

def role_menu():
    while True:
        choice = click.prompt("""
1. Все роли
2. Роль по id
3. Создать роль
4. Обновить роль
5. Удалить роль
6. Назад
""", type=int)
        if choice == 1: all_roles()
        elif choice == 2: role_by_id()
        elif choice == 3: create_r()
        elif choice == 4: update_r()
        elif choice == 5: delete_r()
        elif choice == 6: break
        else: click.echo("1-6")

@click.command()
def cli():
    if not login():
        return
    
    while True:
        choice = click.prompt("""
1. Админы
2. Роли
""", type=int)
        
        if choice == 1:
            admin_menu()
        elif choice == 2:
            role_menu()
        else:
            click.echo("1 или 2")

if __name__ == "__main__":
    cli()