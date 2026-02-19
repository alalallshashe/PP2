def introduce(name, age, city):
    print(f"Меня зовут {name}")
    print(f"Мне {age} лет")
    print(f"Я живу в {city}")

# Вызываем с правильным порядком
introduce("Олег", 20, "Москва")

def create_user(name, job, salary):
    print(f"Имя: {name}")
    print(f"Работа: {job}")
    print(f"Зарплата: {salary}")

# Порядок не важен, когда указываем имена
create_user(salary=50000, name="Мария", job="врач")
create_user(job="учитель", name="Петр", salary=40000)

def order_pizza(dish, size="средняя", topping="сыр"):
    print(f"Заказ: {dish}")
    print(f"Размер: {size}")
    print(f"Добавка: {topping}")
    print("---")

# Можно не указывать size и topping
order_pizza("Маргарита")

# Можно изменить только topping
order_pizza("Пепперони", topping="грибы")

# Можно изменить все
order_pizza("Гавайская", size="большая", topping="ананас")

def print_numbers(*numbers):
    print(f"Получили чисел: {len(numbers)}")
    for num in numbers:
        print(f"Число: {num}")

# Можно передать сколько угодно чисел
print_numbers(1, 2, 3)
print("---")
print_numbers(10, 20, 30, 40, 50)ч