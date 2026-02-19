def greet():
    """Эта функция выводит простое приветствие."""
    print("Привет, мир! Добро пожаловать в мир Python.")

# Вызов функции
greet()
greet()  # Функцию можно вызывать сколько угодно раз



def calculate_sum(a, b):
    """
    Вычисляет сумму двух чисел.
    Аргументы:
        a (int/float): Первое число.
        b (int/float): Второе число.
    Возвращает:
        int/float: Результат сложения.
    """
    result = a + b
    return result

# Использование функции
sum1 = calculate_sum(5, 3)
print(f"Сумма 5 и 3 = {sum1}")

sum2 = calculate_sum(10.5, 2.3)
print(f"Сумма 10.5 и 2.3 = {sum2}")

# Можно использовать результат сразу в выражениях
print(f"Результат * 2 = {calculate_sum(2, 4) * 2}")
def create_profile(name, age, city="Неизвестен"):
    """
    Создает и возвращает строку с профилем пользователя.
    Если город не указан, подставляется значение по умолчанию.
    """
    profile = f"Имя: {name}, Возраст: {age}, Город: {city}"
    return profile

# Вызов с передачей всех аргументов
user1 = create_profile("Анна", 25, "Москва")
print(user1)

# Вызов с аргументом по умолчанию (город будет "Неизвестен")
user2 = create_profile("Иван", 30)
print(user2)

# Вызов с именованными аргументами (порядок не важен)
user3 = create_profile(age=22, name="Ольга", city="Казань")
print(user3)


def is_even(number):
    """
    Проверяет, является ли число четным.
    Возвращает True, если число четное, и False, если нечетное.
    """
    if number % 2 == 0:
        return True
    else:
        return False

# Тестируем функцию
num = 7
if is_even(num):
    print(f"Число {num} четное.")
else:
    print(f"Число {num} нечетное.")

# Используем в цикле
for i in range(1, 6):
    if is_even(i):
        print(f"{i} - четное")
    else:
        print(f"{i} - нечетное")

