numbers = [5, 2, 8, 1, 9, 3]

# Обычная сортировка (по возрастанию)
sorted_asc = sorted(numbers)
print("По возрастанию:", sorted_asc)  # [1, 2, 3, 5, 8, 9]

# Сортировка по убыванию
sorted_desc = sorted(numbers, reverse=True)
print("По убыванию:", sorted_desc)  # [9, 8, 5, 3, 2, 1]

# Сортировка по четности (сначала четные, потом нечетные)
sorted_by_even = sorted(numbers, key=lambda x: x % 2)
print("По четности:", sorted_by_even)  # [2, 8, 4, 1, 3, 5] (примерно)

words = ["яблоко", "банан", "груша", "апельсин", "киви"]

# Сортировка по алфавиту
sorted_alpha = sorted(words)
print("По алфавиту:", sorted_alpha)

# Сортировка по длине слова
sorted_by_length = sorted(words, key=lambda word: len(word))
print("По длине:", sorted_by_length)  # ['киви', 'банан', 'груша', 'яблоко', 'апельсин']

# Сортировка по последней букве
sorted_by_last = sorted(words, key=lambda word: word[-1])
print("По последней букве:", sorted_by_last)

# Сортировка по количеству буквы 'а'
sorted_by_a = sorted(words, key=lambda word: word.count('а'))
print("По количеству 'а':", sorted_by_a)

students = [
    {"name": "Анна", "age": 20, "grade": 85},
    {"name": "Иван", "age": 22, "grade": 92},
    {"name": "Мария", "age": 19, "grade": 78},
    {"name": "Петр", "age": 21, "grade": 88}
]

# Сортировка студентов по возрасту
by_age = sorted(students, key=lambda student: student["age"])
print("По возрасту:")
for s in by_age:
    print(f"  {s['name']}: {s['age']} лет")

# Сортировка по оценкам (от лучших к худшим)
by_grade = sorted(students, key=lambda student: student["grade"], reverse=True)
print("\nПо успеваемости:")
for s in by_grade:
    print(f"  {s['name']}: {s['grade']} баллов")

# Сортировка по имени
by_name = sorted(students, key=lambda student: student["name"])
print("\nПо имени:")
for s in by_name:
    print(f"  {s['name']}")

# Список кортежей (имя, возраст, город)
people = [
    ("Олег", 25, "Москва"),
    ("Анна", 22, "СПб"),
    ("Иван", 30, "Москва"),
    ("Мария", 22, "Казань")
]

# Сортировка по возрасту
by_age = sorted(people, key=lambda person: person[1])
print("По возрасту:")
for name, age, city in by_age:
    print(f"  {name}: {age} лет")

# Сортировка по городу, затем по имени
by_city_name = sorted(people, key=lambda person: (person[2], person[0]))
print("\nПо городу и имени:")
for name, age, city in by_city_name:
    print(f"  {city}: {name}")

# Сортировка точек по расстоянию от начала координат
points = [(1, 2), (3, 1), (2, 3), (0, 1)]
by_distance = sorted(points, key=lambda point: point[0]**2 + point[1]**2)
print("\nТочки по расстоянию:", by_distance)