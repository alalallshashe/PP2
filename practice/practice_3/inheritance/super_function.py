class Animal:
    def __init__(self, name):
        self.name = name
        print(f"Создано животное: {name}")

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)  # вызываем __init__ родителя
        self.breed = breed
        print(f"Порода: {breed}")

# Создаем собаку
my_dog = Dog("Бобик", "дворняжка")
print(f"Имя: {my_dog.name}, Порода: {my_dog.breed}")

class Parent:
    def say_hello(self):
        print("Привет от родителя!")

class Child(Parent):
    def say_hello(self):
        super().say_hello()  # вызываем метод родителя
        print("Привет от ребенка!")

# Вызываем метод
child = Child()
child.say_hello()
# Привет от родителя!
# Привет от ребенка!

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        print(f"Person: {name}, {age}")

class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)  # передаем параметры родителю
        self.student_id = student_id
        print(f"Student ID: {student_id}")

# Создаем студента
s = Student("Анна", 20, "S12345")
print(f"{s.name}, {s.age} лет, ID: {s.student_id}")

class A:
    def __init__(self):
        print("A __init__")

class B(A):
    def __init__(self):
        super().__init__()
        print("B __init__")

class C(B):
    def __init__(self):
        super().__init__()
        print("C __init__")

# Создаем объект C
c = C()
# Выведет:
# A __init__
# B __init__
# C __init__