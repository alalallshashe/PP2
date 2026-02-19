def add_numbers(a, b):
    result = a + b
    return result

# Используем функцию
summa = add_numbers(5, 3)
print(f"Сумма: {summa}")

# Можно сразу использовать результат
print(f"Результат: {add_numbers(10, 20)}")

def is_even(number):
    if number % 2 == 0:
        return True
    else:
        return False

# Проверяем числа
num = 7
if is_even(num):
    print(f"{num} - четное")
else:
    print(f"{num} - нечетное")

# Проверяем несколько чисел
for i in range(1, 6):
    if is_even(i):
        print(f"{i} - четное")

def greet(name):
    return f"Привет, {name}!"

# Создаем приветствия
message1 = greet("Анна")
message2 = greet("Иван")

print(message1)
print(message2)

def get_name_and_age():
    name = "Анна"
    age = 25
    return name, age

# Получаем два значения
user_name, user_age = get_name_and_age()
print(f"Имя: {user_name}")
print(f"Возраст: {user_age}")