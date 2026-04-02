import psycopg2
from config import load_config

def get_connection():
    """ 
    Создает и возвращает объект соединения с PostgreSQL.
    Используется в phonebook.py для вызова функций и процедур.
    """
    config = load_config()
    try:
        # Подключаемся к серверу, используя параметры из database.ini
        conn = psycopg2.connect(**config)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"❌ Ошибка подключения к базе: {error}")
        return None

if __name__ == '__main__':
    # Тестовый запуск: проверяем, работает ли связь
    connection = get_connection()
    if connection:
        print("✅ Соединение с базой данных установлено успешно!")
        connection.close()