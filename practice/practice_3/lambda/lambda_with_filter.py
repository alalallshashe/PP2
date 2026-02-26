numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Оставляем только четные числа
evens = list(filter(lambda x: x % 2 == 0, numbers))
print("Четные:", evens)  # [2, 4, 6, 8, 10]

# Оставляем только нечетные числа
odds = list(filter(lambda x: x % 2 != 0, numbers))
print("Нечетные:", odds)  # [1, 3, 5, 7, 9]

# Числа больше 5
big_numbers = list(filter(lambda x: x > 5, numbers))
print("Больше 5:", big_numbers)  # [6, 7, 8, 9, 10]

words = ["кот", "собака", "дом", "автомобиль", "лес", "университет"]

# Слова длиной больше 3 букв
long_words = list(filter(lambda word: len(word) > 3, words))
print("Длинные слова:", long_words)  # ['собака', 'автомобиль', 'университет']

# Слова начинающиеся на 'а'
a_words = list(filter(lambda word: word.startswith('а'), words))
print("Начинаются на 'а':", a_words)  # ['автомобиль']

# Слова содержащие букву 'о'
o_words = list(filter(lambda word: 'о' in word, words))
print("Содержат 'о':", o_words)  # ['кот', 'собака', 'дом', 'автомобиль']

mixed = [10, "привет", 0, "мир", 15, "", "python", None, 7]

# Оставляем только числа
numbers_only = list(filter(lambda x: isinstance(x, (int, float)), mixed))
print("Только числа:", numbers_only)  # [10, 0, 15, 7]

# Оставляем только непустые строки
strings_only = list(filter(lambda x: isinstance(x, str) and x != "", mixed))
print("Только строки:", strings_only)  # ['привет', 'мир', 'python']

# Оставляем все, что не None и не пустая строка
valid_data = list(filter(lambda x: x is not None and x != "", mixed))
print("Все кроме None и пустых строк:", valid_data)  # [10, 'привет', 'мир', 15, 'python', 7]

# Фильтрация оценок студентов (только проходные баллы)
grades = [85, 45, 92, 38, 76, 51, 63, 29]
passing = list(filter(lambda grade: grade >= 60, grades))
print("Сдали экзамен:", passing)  # [85, 92, 76, 63]

# Фильтрация цен (только доступные товары)
products = [
    {"name": "телефон", "price": 50000},
    {"name": "книга", "price": 500},
    {"name": "ноутбук", "price": 80000},
    {"name": "ручка", "price": 50}
]

# Товары дешевле 1000 рублей
cheap = list(filter(lambda item: item["price"] < 1000, products))
print("Дешевые товары:")
for item in cheap:
    print(f"  {item['name']}: {item['price']} руб.")

# Фильтрация списка email (только с доменом .ru)
emails = ["user@gmail.com", "info@yandex.ru", "test@mail.ru", "admin@yahoo.com"]
ru_emails = list(filter(lambda email: email.endswith(".ru"), emails))
print("\nEmail с .ru:", ru_emails)  # ['info@yandex.ru', 'test@mail.ru']