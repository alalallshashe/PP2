def greet(name, age):
    print(f"Привет, {name}!")
    print(f"Тебе {age} лет")

# Важен порядок аргументов
greet("Анна", 25)
greet("Иван", 30)

def create_profile(name, job, city):
    print(f"Имя: {name}")
    print(f"Работа: {job}")
    print(f"Город: {city}")

# Можно указывать в любом порядке
create_profile(city="Москва", name="Олег", job="врач")
create_profile(job="учитель", name="Мария", city="СПб")

def order_coffee(size="средний", sugar=True, milk=False):
    print(f"Кофе: {size}")
    print(f"Сахар: {'да' if sugar else 'нет'}")
    print(f"Молоко: {'да' if milk else 'нет'}")
    print("---")

# Можно не указывать все аргументы
order_coffee()                          # все по умолчанию
order_coffee("большой")                  # только размер
order_coffee(milk=True, size="маленький") # именованные

def student_info(name, age, city="Неизвестен", course=1):
    print(f"Студент: {name}")
    print(f"Возраст: {age}")
    print(f"Город: {city}")
    print(f"Курс: {course}")
    print("---")

# Разные способы вызова
student_info("Анна", 20)                          # только обязательные
student_info("Иван", 22, "Москва")                # с городом
student_info("Петр", 19, course=2)                 # с курсом
student_info(age=21, name="Мария", city="Казань") # именованные