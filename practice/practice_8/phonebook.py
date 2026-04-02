import psycopg2
from config import load_config

def connect():
    config = load_config()
    return psycopg2.connect(**config)

def setup_database():
    """Скрытая настройка базы данных при запуске"""
    commands = [
        "CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT) RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$ BEGIN RETURN QUERY SELECT contact_id, first_name, phone_number FROM contacts ORDER BY contact_id LIMIT p_limit OFFSET p_offset; END; $$ LANGUAGE plpgsql;",
        "CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR) LANGUAGE plpgsql AS $$ BEGIN IF EXISTS (SELECT 1 FROM contacts WHERE first_name = p_name) THEN UPDATE contacts SET phone_number = p_phone WHERE first_name = p_name; ELSE INSERT INTO contacts(first_name, phone_number) VALUES(p_name, p_phone); END IF; END; $$;",
        "CREATE OR REPLACE FUNCTION find_contacts(p_pat TEXT) RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$ BEGIN RETURN QUERY SELECT contact_id, first_name, phone_number FROM contacts WHERE first_name ILIKE '%' || p_pat || '%' OR phone_number LIKE p_pat || '%'; END; $$ LANGUAGE plpgsql;",
        "CREATE OR REPLACE PROCEDURE delete_contact(p_target VARCHAR) LANGUAGE plpgsql AS $$ BEGIN DELETE FROM contacts WHERE first_name = p_target OR phone_number = p_target; END; $$;"
    ]
    with connect() as conn:
        with conn.cursor() as cur:
            for cmd in commands: cur.execute(cmd)
        conn.commit()

def show_all():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_paginated(10, 0);")
            rows = cur.fetchall()
            print("\n--- СПИСОК КОНТАКТОВ ---")
            for r in rows: print(f"{r[1]}: {r[2]}")

def main():
    setup_database()
    while True:
        print("\n[1] Показать [2] Найти [3] Добавить [4] Удалить [0] Выход")
        cmd = input("Выбор > ")

        if cmd == '1':
            show_all()
        elif cmd == '2':
            pat = input("Имя или номер: ")
            with connect() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM find_contacts(%s);", (pat,))
                    for r in cur.fetchall(): print(f"Найдено: {r[1]} ({r[2]})")
        elif cmd == '3':
            n, p = input("Имя: "), input("Телефон: ")
            with connect() as conn:
                with conn.cursor() as cur:
                    cur.execute("CALL upsert_contact(%s, %s);", (n, p))
                    conn.commit()
            print("Готово.")
        elif cmd == '4':
            target = input("Имя или номер для удаления: ")
            with connect() as conn:
                with conn.cursor() as cur:
                    cur.execute("CALL delete_contact(%s);", (target,))
                    conn.commit()
            print("Удалено.")
        elif cmd == '0':
            print("Выход...")
            break
        else:
            print("Ошибка: выберите число от 0 до 4")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Ошибка подключения: {e}")