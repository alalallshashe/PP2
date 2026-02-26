class Person:
    def __init__(self, name):
        self.name = name

# Создаем людей
p1 = Person("Анна")
p2 = Person("Иван")

print(p1.name)  # Анна
print(p2.name)  # Иван

class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# Создаем собак
dog1 = Dog("Бобик", 3)
dog2 = Dog("Шарик", 5)

print(f"{dog1.name}, {dog1.age} года")
print(f"{dog2.name}, {dog2.age} лет")

class Car:
    def __init__(self, brand, color="белый"):
        self.brand = brand
        self.color = color

# Можно не указывать цвет
car1 = Car("Toyota")
car2 = Car("BMW", "черный")

print(f"{car1.brand} - {car1.color}")
print(f"{car2.brand} - {car2.color}")

class Student:
    def __init__(self, name):
        self.name = name
        self.grades = []  # пустой список для оценок
        print(f"Создан студент: {name}")

# Создаем студента (сразу видим сообщение)
s = Student("Мария")
print(f"Оценки: {s.grades}")  # пустой список