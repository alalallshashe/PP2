#1exaple
# min, max - минимум и максимум
numbers = [5, 2, 8, 1, 9]
print(min(numbers))  # 1
print(max(numbers))  # 9

# abs - абсолютное значение
print(abs(-7))       # 7
print(abs(3.14))     # 3.14

# round - округление
print(round(3.14159, 2))  # 3.14
print(round(4.7))         # 5

# pow - возведение в степень
print(pow(2, 3))     # 8 (2³)
print(2 ** 3)        # 8 (альтернатива)

#2example
import math

# Константы
print(math.pi)       # 3.141592653589793
print(math.e)        # 2.718281828459045

# Корень числа
print(math.sqrt(16)) # 4.0
print(math.sqrt(2))  # 1.4142135623730951

# Округление
print(math.floor(3.7))  # 3 (вниз)
print(math.ceil(3.1))   # 4 (вверх)

# Степени и логарифмы
print(math.pow(2, 3))   # 8.0
print(math.log(100, 10)) # 2.0

#3example
import math

# Перевод градусов в радианы
angle_deg = 60
angle_rad = math.radians(angle_deg)

# Тригонометрические функции
print(math.sin(angle_rad))      # 0.8660254037844386
print(math.cos(angle_rad))      # 0.5
print(math.tan(angle_rad))      # 1.7320508075688767

# Обратные функции
print(math.degrees(math.asin(0.5)))  # 30.0

#4example
import random

# random() - число от 0 до 1
print(random.random())        # 0.374540114...

# randint() - целое в диапазоне
print(random.randint(1, 10))  # 7 (случайное от 1 до 10)

# uniform() - дробное в диапазоне
print(random.uniform(5, 10))  # 7.832156...

# choice() - случайный элемент
colors = ["красный", "синий", "зеленый"]
print(random.choice(colors))  # синий

# shuffle() - перемешивание списка
cards = ["туз", "король", "дама", "валет"]
random.shuffle(cards)
print(cards)  # ['дама', 'туз', 'валет', 'король']