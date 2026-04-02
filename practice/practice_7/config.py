from configparser import ConfigParser
import os

def load_config(filename='database.ini', section='postgresql'):
    # Создаем объект для чтения .ini файлов
    parser = ConfigParser()
    
    # Читаем файл
    if not os.path.exists(filename):
        raise Exception(f'Файл {filename} не найден! Убедись, что он в той же папке.')
        
    parser.read(filename)

    # Получаем настройки из секции [postgresql]
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(f'Секция [{section}] не найдена в файле {filename}')

    return config