class Animal:
    def make_sound(self):
        print("Животное издает звук")

class Cat(Animal):
    def make_sound(self):  # переопределяем метод
        print("Мяу!")

class Dog(Animal):
    def make_sound(self):  # переопределяем метод
        print("Гав!")

# Создаем животных
animal = Animal()
cat = Cat()
dog = Dog()

animal.make_sound()  # Животное издает звук
cat.make_sound()     # Мяу!
dog.make_sound()     # Гав!

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __str__(self):  # переопределяем стандартный метод
        return f"Person: {self.name}, {self.age} лет"

# Создаем человека
p = Person("Анна", 25)
print(p)  # Person: Анна, 25 лет (вместо <__main__.Person object...>)

class Vehicle:
    def start(self):
        print("Двигатель запущен")

class Car(Vehicle):
    def start(self):  # переопределяем
        super().start()  # вызываем родительский метод
        print("Машина готова к поездке!")

# Создаем машину
my_car = Car()
my_car.start()
# Двигатель запущен
# Машина готова к поездке!

class Shape:
    def area(self):
        return 0

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):  # переопределяем
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):  # переопределяем
        return 3.14 * self.radius ** 2

# Создаем фигуры
rect = Rectangle(5, 3)
circle = Circle(2)

print(f"Площадь прямоугольника: {rect.area()}")  # 15
print(f"Площадь круга: {circle.area()}")         # 12.56
print(f"Площадь фигуры: {Shape().area()}")       # 0