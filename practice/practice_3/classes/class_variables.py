class Dog:
    # Переменная класса (общая для всех собак)
    total_dogs = 0
    
    def __init__(self, name):
        self.name = name  # переменная объекта
        Dog.total_dogs += 1  # увеличиваем общий счетчик

# Создаем собак
dog1 = Dog("Бобик")
print(f"Всего собак: {Dog.total_dogs}")  # 1

dog2 = Dog("Шарик")
print(f"Всего собак: {Dog.total_dogs}")  # 2

dog3 = Dog("Рекс")
print(f"Всего собак: {Dog.total_dogs}")  # 3

class Student:
    # Переменные класса
    school = "Школа №1"
    city = "Москва"
    
    def __init__(self, name):
        self.name = name  # переменная объекта
    
    def info(self):
        print(f"Студент: {self.name}")
        print(f"Школа: {Student.school}")
        print(f"Город: {Student.city}")

# Все студенты учатся в одной школе
s1 = Student("Анна")
s2 = Student("Иван")

s1.info()
print("---")
s2.info()

class Car:
    # Переменная класса
    wheels = 4
    
    def __init__(self, color):
        self.color = color  # переменная объекта

# Создаем машины
car1 = Car("красный")
car2 = Car("синий")

print(f"У машин {Car.wheels} колеса")  # 4

# Меняем переменную класса для всех машин
Car.wheels = 6
print(f"Теперь у машин {Car.wheels} колес")  # 6

# У каждой машины свой цвет
print(f"{car1.color} машина")  # красный
print(f"{car2.color} машина")  # синий

class Math:
    # Переменные класса как константы
    PI = 3.14159
    E = 2.71828
    
    def __init__(self, value):
        self.value = value
    
    def circle_area(self, radius):
        return Math.PI * radius ** 2

# Используем константы
print(f"Число Пи: {Math.PI}")
print(f"Число E: {Math.E}")

m = Math(10)
print(f"Площадь круга: {m.circle_area(5)}")