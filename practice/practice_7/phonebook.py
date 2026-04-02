import psycopg2
import csv
from config import load_config

def connect():
    """Подключение к базе данных"""
    config = load_config()
    return psycopg2.connect(**config)

def create_table():
    """Создание таблицы (Задание 3.2.1)"""
    sql = """
    CREATE TABLE IF NOT EXISTS contacts (
        contact_id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50),
        phone_number VARCHAR(20) UNIQUE NOT NULL
    );
    """
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                conn.commit()
                print("--- Таблица проверена/создана ---")
    except Exception as e:
        print(f"Ошибка при создании таблицы: {e}")

def import_csv(filename):
    """Импорт данных из CSV (Задание 3.2.2)"""
    sql = "INSERT INTO contacts (first_name, phone_number) VALUES (%s, %s) ON CONFLICT (phone_number) DO NOTHING;"
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                with open(filename, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader)  # Пропуск заголовка
                    cur.executemany(sql, list(reader))
                conn.commit()
                print("--- Данные из CSV успешно импортированы ---")
    except Exception as e:
        print(f"Ошибка при импорте CSV: {e}")

def add_from_console():
    """Добавление через консоль (Задание 3.2.3)"""
    name = input("Введите имя: ")
    phone = input("Введите телефон: ")
    sql = "INSERT INTO contacts (first_name, phone_number) VALUES (%s, %s) ON CONFLICT (phone_number) DO NOTHING;"
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (name, phone))
            conn.commit()
            print(f"Контакт {name} обработан.")

def update_contact():
    """Обновление (Задание 3.2.4)"""
    name = input("Имя контакта для обновления: ")
    new_phone = input("Новый номер телефона: ")
    sql = "UPDATE contacts SET phone_number = %s WHERE first_name = %s;"
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (new_phone, name))
            conn.commit()
            print("Данные обновлены.")

def find_contacts():
    """Поиск (Задание 3.2.5)"""
    pattern = input("Введите имя или начало телефона для поиска: ")
    sql = "SELECT * FROM contacts WHERE first_name ILIKE %s OR phone_number LIKE %s;"
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (f'%{pattern}%', f'{pattern}%'))
            rows = cur.fetchall()
            if not rows:
                print("Ничего не найдено.")
            else:
                for row in rows:
                    print(f"ID: {row[0]} | Имя: {row[1]} | Телефон: {row[3]}")

def delete_contact():
    """Удаление (Задание 3.2.6)"""
    target = input("Введите имя или телефон для удаления: ")
    sql = "DELETE FROM contacts WHERE first_name = %s OR phone_number = %s;"
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (target, target))
            conn.commit()
            print("Запись удалена.")

# --- ФИНАЛЬНЫЙ БЛОК С ПРАВИЛЬНЫМИ ОТСТУПАМИ ---
if __name__ == "__main__":
    create_table()
    import_csv('contacts.csv')
    
    while True:
        print("\n--- PhoneBook Меню ---")
        print("1. Добавить  2. Найти  3. Обновить  4. Удалить  5. Выход")
        choice = input("Выберите действие (1-5): ")
        
        if choice == '1':
            add_from_console()
        elif choice == '2':
            find_contacts()
        elif choice == '3':
            update_contact()
        elif choice == '4':
            delete_contact()
        elif choice == '5':
            print("Выход из программы...")
            break
        else:
            print("Неверный выбор, попробуйте снова.")