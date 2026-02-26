# Обычная функция
def add_usual(x, y):
    return x + y

# Лямбда-функция
add_lambda = lambda x, y: x + y

# Используем обе
print(add_usual(5, 3))    # 8
print(add_lambda(5, 3))    # 8

# Можно использовать без присваивания
print((lambda x, y: x + y)(10, 20))  # 30

# Удвоение числа
double = lambda x: x * 2
print(double(5))      # 10
print(double(10))     # 20

# Квадрат числа
square = lambda x: x ** 2
print(square(4))      # 16
print(square(7))      # 49

# Приветствие
greet = lambda name: f"Привет, {name}!"
print(greet("Анна"))  # Привет, Анна!

# Простая проверка
is_even = lambda x: x % 2 == 0
print(is_even(4))    # True
print(is_even(7))    # False

# Больше или меньше
compare = lambda x, y: f"{x} больше {y}" if x > y else f"{x} меньше {y}"
print(compare(10, 5))   # 10 больше 5
print(compare(3, 8))    # 3 меньше 8

# Проверка возраста
can_vote = lambda age: "Можно голосовать" if age >= 18 else "Нельзя голосовать"
print(can_vote(20))  # Можно голосовать
print(can_vote(16))  # Нельзя голосовать

numbers = [1, 2, 3, 4, 5]

# Удваиваем все числа с помощью map
doubled = list(map(lambda x: x * 2, numbers))
print("Удвоенные:", doubled)  # [2, 4, 6, 8, 10]

# Оставляем только четные числа с помощью filter
evens = list(filter(lambda x: x % 2 == 0, numbers))
print("Четные:", evens)  # [2, 4]

# Другой пример с именами
names = ["анна", "иван", "мария", "петр"]
upper_names = list(map(lambda name: name.title(), names))
print("Имена:", upper_names)  # ['Анна', 'Иван', 'Мария', 'Петр']