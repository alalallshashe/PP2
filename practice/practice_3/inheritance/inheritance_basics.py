class Animal:  # Родительский класс
    def __init__(self, name):
        self.name = name
    
    def eat(self):
        print(f"{self.name} ест")

class Dog(Animal):  # Дочерний класс (наследует от Animal)
    def bark(self):
        print(f"{self.name} говорит Гав!")

# Создаем собаку
my_dog = Dog("Бобик")
my_dog.eat()   # метод от родителя
my_dog.bark()  # свой метод 

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def introduce(self):
        print(f"Я {self.name}, мне {self.age} лет")

class Student(Person):
    def __init__(self, name, age, school):
        super().__init__(name, age)  # вызываем __init__ родителя
        self.school = school  # новый атрибут
    
    def study(self):
        print(f"{self.name} учится в {self.school}")

# Создаем студента
s = Student("Анна", 20, "МГУ")
s.introduce()  # метод от родителя
s.study()      # свой метод

class Animal:
    def make_sound(self):
        print("Какое-то животное издает звук")

class Cat(Animal):
    def make_sound(self):  # переопределяем метод
        print("Мяу!")

class Dog(Animal):
    def make_sound(self):  # переопределяем метод
        print("Гав!")

# Создаем животных
cat = Cat()
dog = Dog()
animal = Animal()

cat.make_sound()   # Мяу!
dog.make_sound()   # Гав!
animal.make_sound()  # Какое-то животное издает звук

class Flyer:
    def fly(self):
        print("Я лечу!")

class Swimmer:
    def swim(self):
        print("Я плыву!")

class Duck(Flyer, Swimmer):  # наследует от двух классов
    def sound(self):
        print("Кря!")

# Утка умеет все
duck = Duck()
duck.fly()    # от Flyer
duck.swim()   # от Swimmer
duck.sound()  # свой метод