numbers = [1, 2, 3, 4, 5]

# Умножаем каждое число на 2
doubled = list(map(lambda x: x * 2, numbers))
print("Оригинал:", numbers)
print("Удвоено:", doubled)

# Возводим в квадрат
squared = list(map(lambda x: x ** 2, numbers))
print("В квадрате:", squared)

names = ["анна", "иван", "мария", "петр"]

# Делаем первую букву заглавной
capitalized = list(map(lambda name: name.title(), names))
print("С заглавной:", capitalized)

# Переводим в верхний регистр
upper_names = list(map(lambda name: name.upper(), names))
print("Верхний регистр:", upper_names)

# Добавляем приветствие
greetings = list(map(lambda name: f"Привет, {name.title()}!", names))
print(greetings)

# Складываем элементы двух списков
a = [1, 2, 3]
b = [10, 20, 30]

sums = list(map(lambda x, y: x + y, a, b))
print(f"{a} + {b} = {sums}")

# Умножаем элементы двух списков
products = list(map(lambda x, y: x * y, a, b))
print(f"{a} * {b} = {products}")

# Конвертация температуры из Цельсия в Фаренгейты
celsius = [0, 20, 30, 40]
fahrenheit = list(map(lambda c: (c * 9/5) + 32, celsius))
print("Цельсий:", celsius)
print("Фаренгейт:", fahrenheit)

# Вычисление длины строк
fruits = ["яблоко", "банан", "апельсин", "киви"]
lengths = list(map(lambda fruit: len(fruit), fruits))
print("Фрукты:", fruits)
print("Длины:", lengths)

# Округление чисел
prices = [10.567, 23.491, 5.123, 8.999]
rounded = list(map(lambda price: round(price, 2), prices))
print("Цены:", prices)
print("Округлено:", rounded)