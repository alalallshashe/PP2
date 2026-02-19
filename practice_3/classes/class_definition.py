class Cat:
    def __init__(self, name):
        self.name = name
    
    def meow(self):
        print(f"{self.name}: Мяу!")

# Создаем котов
cat1 = Cat("Барсик")
cat2 = Cat("Мурка")

cat1.meow()  # Барсик: Мяу!
cat2.meow()  # Мурка: Мяу!

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
    
    def info(self):
        print(f"Книга: {self.title}")
        print(f"Автор: {self.author}")

# Создаем книги
book1 = Book("Война и мир", "Толстой")
book2 = Book("Преступление и наказание", "Достоевский")

book1.info()
print("---")
book2.info()

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def hello(self):
        print(f"Привет! Я {self.name}")
    
    def birthday(self):
        self.age += 1
        print(f"{self.name} теперь {self.age} лет!")

# Создаем студента
s = Student("Анна", 20)
s.hello()        # Привет! Я Анна
s.birthday()     # Анна теперь 21 лет!

class Calculator:
    def add(self, a, b):
        return a + b
    
    def mult(self, a, b):
        return a * b

# Используем калькулятор
calc = Calculator()
print(f"5 + 3 = {calc.add(5, 3)}")
print(f"5 * 3 = {calc.mult(5, 3)}")