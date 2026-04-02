import psycopg2
from config import load_config

def connect():
    """Подключение к базе данных через твой config.py"""
    try:
        config = load_config()
        conn = psycopg2.connect(**config)
        conn.autocommit = True
        return conn
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        exit()

def setup_db(cur):
    """Создание таблиц, функций и процедур"""
    # 1. Основная таблица
    cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        phone VARCHAR(20)
    );
    """)

    # 2. Функция поиска по шаблону
    cur.execute("""
    CREATE OR REPLACE FUNCTION search_pattern(p_pattern TEXT)
    RETURNS TABLE(id INT, first_name VARCHAR, last_name VARCHAR, phone VARCHAR) AS $$
    BEGIN
        RETURN QUERY
        SELECT * FROM phonebook
        WHERE phonebook.first_name ILIKE '%' || p_pattern || '%'
           OR phonebook.last_name ILIKE '%' || p_pattern || '%'
           OR phonebook.phone ILIKE '%' || p_pattern || '%';
    END;
    $$ LANGUAGE plpgsql;
    """)

    # 3. Процедура вставки или обновления
    cur.execute("""
    CREATE OR REPLACE PROCEDURE insert_or_update(p_first TEXT, p_last TEXT, p_phone TEXT)
    AS $$
    BEGIN
        IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_first AND last_name = p_last) THEN
            UPDATE phonebook SET phone = p_phone WHERE first_name = p_first AND last_name = p_last;
        ELSE
            INSERT INTO phonebook(first_name, last_name, phone) VALUES (p_first, p_last, p_phone);
        END IF;
    END;
    $$ LANGUAGE plpgsql;
    """)

    # 4. Временная таблица и процедура массовой вставки
    cur.execute("CREATE TEMP TABLE IF NOT EXISTS temp_users(first_name VARCHAR(50), last_name VARCHAR(50), phone VARCHAR(20));")
    
    cur.execute("""
    CREATE OR REPLACE PROCEDURE insert_many_proc()
    AS $$
    DECLARE
        rec RECORD;
    BEGIN
        FOR rec IN SELECT * FROM temp_users LOOP
            IF rec.phone ~ '^[0-9]+$' THEN
                INSERT INTO phonebook(first_name, last_name, phone)
                VALUES (rec.first_name, rec.last_name, rec.phone);
            ELSE
                RAISE NOTICE 'Некорректный номер: %', rec.phone;
            END IF;
        END LOOP;
    END;
    $$ LANGUAGE plpgsql;
    """)

    # 5. Функция пагинации
    cur.execute("""
    CREATE OR REPLACE FUNCTION get_paginated(p_limit INT, p_offset INT)
    RETURNS TABLE(id INT, first_name VARCHAR, last_name VARCHAR, phone VARCHAR) AS $$
    BEGIN
        RETURN QUERY
        SELECT * FROM phonebook
        ORDER BY id
        LIMIT p_limit OFFSET p_offset;
    END;
    $$ LANGUAGE plpgsql;
    """)

    # 6. Процедура удаления
    cur.execute("""
    CREATE OR REPLACE PROCEDURE delete_user(p_value TEXT)
    AS $$
    BEGIN
        DELETE FROM phonebook
        WHERE first_name = p_value OR last_name = p_value OR phone = p_value;
    END;
    $$ LANGUAGE plpgsql;
    """)

# --- Функции для работы с пользователем ---

def add_user(cur):
    f = input("Имя: ")
    l = input("Фамилия: ")
    p = input("Телефон: ")
    cur.execute("CALL insert_or_update(%s, %s, %s)", (f, l, p))
    print("✅ Запись добавлена или обновлена.")

def add_many(cur):
    try:
        val = input("Сколько контактов добавить? ")
        if not val: return
        n = int(val)
        cur.execute("DELETE FROM temp_users")
        for _ in range(n):
            f = input("Имя: ")
            l = input("Фамилия: ")
            p = input("Телефон: ")
            cur.execute("INSERT INTO temp_users VALUES (%s, %s, %s)", (f, l, p))
        cur.execute("CALL insert_many_proc()")
        print("✅ Массовая вставка завершена.")
    except ValueError:
        print("❌ Ошибка: Введите число.")

def search(cur):
    pattern = input("Введите текст для поиска: ")
    cur.execute("SELECT * FROM search_pattern(%s)", (pattern,))
    rows = cur.fetchall()
    if not rows:
        print("Ничего не найдено.")
    for r in rows:
        print(f"ID {r[0]}: {r[1]} {r[2]} — {r[3]}")

def paginate(cur):
    try:
        lim = input("Лимит (сколько записей): ")
        off = input("Смещение (пропустить сколько): ")
        if not lim or not off: return
        cur.execute("SELECT * FROM get_paginated(%s, %s)", (int(lim), int(off)))
        rows = cur.fetchall()
        for r in rows:
            print(f"ID {r[0]}: {r[1]} {r[2]} — {r[3]}")
    except ValueError:
        print("❌ Ошибка: Введите числа.")

def delete(cur):
    val = input("Кого удалить (имя/фамилия/номер): ")
    cur.execute("CALL delete_user(%s)", (val,))
    print("✅ Запрос на удаление выполнен.")

def show_all(cur):
    cur.execute("SELECT * FROM phonebook ORDER BY id")
    rows = cur.fetchall()
    if not rows:
        print("База пуста.")
    for r in rows:
        print(f"ID {r[0]}: {r[1]} {r[2]} — {r[3]}")

def main():
    conn = connect()
    cur = conn.cursor()
    setup_db(cur)

    while True:
        print("\n--- МЕНЮ ---")
        print("1 - Добавить/Обновить")
        print("2 - Добавить много (Mass)")
        print("3 - Поиск")
        print("4 - Пагинация")
        print("5 - Удалить")
        print("6 - Показать всех")
        print("0 - Выход")
        
        choice = input(">> ")
        if choice == "1": add_user(cur)
        elif choice == "2": add_many(cur)
        elif choice == "3": search(cur)
        elif choice == "4": paginate(cur)
        elif choice == "5": delete(cur)
        elif choice == "6": show_all(cur)
        elif choice == "0": break
        else: print("Неверный выбор.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()