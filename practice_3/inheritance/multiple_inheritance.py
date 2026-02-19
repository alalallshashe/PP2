class Flyer:
    def fly(self):
        print("Я лечу!")

class Swimmer:
    def swim(self):
        print("Я плыву!")

class Duck(Flyer, Swimmer):  # наследует от двух классов
    def quack(self):
        print("Кря-кря!")

# Утка умеет всё
duck = Duck()
duck.fly()    # от Flyer
duck.swim()   # от Swimmer
duck.quack()  # свой метод  

class A:
    def say(self):
        print("Привет от A")

class B:
    def say(self):
        print("Привет от B")

class C(A, B):  # сначала A, потом B
    pass

class D(B, A):  # сначала B, потом A
    pass

c = C()
c.say()  # Привет от A (первый родитель)

d = D()
d.say()  # Привет от B (первый родитель)    

class Father:
    def __init__(self, name):
        self.father_name = name
        print(f"Отец: {name}")

class Mother:
    def __init__(self, name):
        self.mother_name = name
        print(f"Мать: {name}")

class Child(Father, Mother):
    def __init__(self, name, father_name, mother_name):
        Father.__init__(self, father_name)
        Mother.__init__(self, mother_name)
        self.child_name = name
        print(f"Ребенок: {name}")
    
    def introduce(self):
        print(f"Я {self.child_name}, сын {self.father_name} и {self.mother_name}")

# Создаем ребенка
child = Child("Петя", "Иван", "Мария")
child.introduce()

class Developer:
    def __init__(self, language):
        self.language = language
    
    def code(self):
        print(f"Пишу код на {self.language}")

class Manager:
    def __init__(self, team_size):
        self.team_size = team_size
    
    def manage(self):
        print(f"Управляю командой из {self.team_size} человек")

class TechLead(Developer, Manager):
    def __init__(self, language, team_size, name):
        Developer.__init__(self, language)
        Manager.__init__(self, team_size)
        self.name = name
    
    def work(self):
        print(f"Я {self.name} - TechLead")
        self.code()
        self.manage()

# Создаем тимлида
tl = TechLead("Python", 5, "Анна")
tl.work()