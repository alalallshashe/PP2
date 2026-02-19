def sum_all(*args):
    total = 0
    for num in args:
        total += num
    return total

# Можно передать любое количество чисел
print(sum_all(1, 2))           # 3
print(sum_all(1, 2, 3, 4, 5))  # 15
print(sum_all(10, 20))          # 30

def print_all(*args):
    count = 1
    for item in args:
        print(f"Аргумент {count}: {item}")
        count += 1

# Можно передавать любые значения
print_all("яблоко", 42, True, 3.14)
print("---")
print_all(1, 2, 3)

def show_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

# Передаем именованные аргументы
show_info(name="Анна", age=25, city="Москва")
print("---")
show_info(product="телефон", price=50000, in_stock=True)

def my_function(*args, **kwargs):
    print("Позиционные аргументы:", args)
    print("Именованные аргументы:", kwargs)
    print("---")

# Вызываем с разными аргументами
my_function(1, 2, 3)
my_function(a=1, b=2)
my_function(1, 2, name="Дима", age=30)