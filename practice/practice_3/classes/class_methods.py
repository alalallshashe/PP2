class Dog:
    def __init__(self, name):
        self.name = name
    
    def bark(self):  # простой метод
        print(f"{self.name}: Гав!")
    
    def sleep(self):  # еще один метод
        print(f"{self.name} спит...")

# Создаем собаку
my_dog = Dog("Бобик")
my_dog.bark()   # Бобик: Гав!
my_dog.sleep()  # Бобик спит...

class Calculator:
    def __init__(self, name):
        self.name = name
    
    def add(self, a, b):
        result = a + b
        print(f"{self.name}: {a} + {b} = {result}")
        return result
    
    def multiply(self, a, b):
        result = a * b
        print(f"{self.name}: {a} * {b} = {result}")
        return result

# Используем калькулятор
calc = Calculator("Мой калькулятор")
calc.add(5, 3)        # Мой калькулятор: 5 + 3 = 8
calc.multiply(4, 2)    # Мой калькулятор: 4 * 2 = 8

class Counter:
    def __init__(self):
        self.count = 0
    
    def increment(self):  # увеличивает счетчик
        self.count += 1
        print(f"Счетчик: {self.count}")
    
    def reset(self):  # сбрасывает счетчик
        self.count = 0
        print("Счетчик сброшен")

# Работаем со счетчиком
c = Counter()
c.increment()  # Счетчик: 1
c.increment()  # Счетчик: 2
c.reset()      # Счетчик сброшен
c.increment()  # Счетчик: 1

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):  # возвращает площадь
        return self.width * self.height
    
    def perimeter(self):  # возвращает периметр
        return 2 * (self.width + self.height)

# Создаем прямоугольник
rect = Rectangle(5, 3)
print(f"Площадь: {rect.area()}")        # Площадь: 15
print(f"Периметр: {rect.perimeter()}")  # Периметр: 16