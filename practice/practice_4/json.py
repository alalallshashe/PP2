import json

# JSON строка -> Python объект
json_data = '{"name": "Анна", "age": 25, "hobbies": ["чтение", "спорт"]}'
python_obj = json.loads(json_data)

print(python_obj["name"])      # Анна
print(python_obj["age"])       # 25
print(python_obj["hobbies"])   # ['чтение', 'спорт']

#2example

import json

# Python объект -> JSON строка
person = {
    "name": "Петр",
    "age": 30,
    "is_student": False,
    "grades": [4, 5, 3]
}

json_string = json.dumps(person)
print(json_string)  # {"name": "\u041f\u0435\u0442\u0440", "age": 30, "is_student": false, "grades": [4, 5, 3]}

# С отступами и без экранирования Unicode
json_pretty = json.dumps(person, indent=2, ensure_ascii=False)
print(json_pretty)

#3example
import json

data = {
    "city": "Москва",
    "temperature": 20.5,
    "units": "celsius"
}

with open("weather.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2, ensure_ascii=False)
# Файл создан с отформатированным JSON

#4example

import json

with open("weather.json", "r", encoding="utf-8") as file:
    loaded_data = json.load(file)

print(loaded_data["city"])         # Москва
print(loaded_data["temperature"])  # 20.5

#5example
import json

# Python типы -> JSON типы
data = {
    "string": "текст",
    "number_int": 100,
    "number_float": 3.14,
    "boolean_true": True,
    "boolean_false": False,
    "none_value": None,
    "list": [1, 2, 3],
    "dict": {"key": "value"}
}

json_str = json.dumps(data, indent=2, ensure_ascii=False)
print(json_str)
# Обратите внимание: None -> null, True/False -> true/false

#6example
import json

# Создаем простой sample-data.json
sample = {
    "users": [
        {"id": 1, "name": "Иван", "age": 25},
        {"id": 2, "name": "Мария", "age": 30}
    ]
}

# Записываем
with open("sample-data.json", "w", encoding="utf-8") as f:
    json.dump(sample, f, indent=2, ensure_ascii=False)

# Читаем и выводим имена
with open("sample-data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for user in data["users"]:
    print(f"{user['id']}: {user['name']}, {user['age']} лет")
# 1: Иван, 25 лет
# 2: Мария, 30 лет