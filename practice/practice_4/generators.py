# Создаем итератор из списка
my_list = [10, 20, 30]
my_iterator = iter(my_list)

# Вручную получаем элементы с помощью next()
print(next(my_iterator))  # Вывод: 10
print(next(my_iterator))  # Вывод: 20
print(next(my_iterator))  # Вывод: 30

# Следующий вызов вызовет ошибку StopIteration, так как элементов больше нет
# print(next(my_iterator)) # Раскомментируйте, чтобы увидеть ошибку

class FibonacciIterator:                                             ##2example
    """Итератор для последовательности Фибоначчи до n-го числа."""
    def __init__(self, n):
        self.n = n          # Количество чисел Фибоначчи для генерации
        self.current = 0    # Первое число
        self.next = 1       # Второе число
        self.count = 0      # Счетчик сгенерированных чисел

    def __iter__(self):
        return self

    def __next__(self):
        self.count += 1
        if self.count > self.n:
            raise StopIteration
        if self.count == 1:
            return self.current
        # Рассчитываем следующее число
        self.current, self.next = self.next, self.current + self.next
        return self.current

# Используем итератор в цикле for
fib_iter = FibonacciIterator(7)
for num in fib_iter:
    print(num, end=" ") # Вывод: 0 1 1 2 3 5 8

def even_numbers_up_to(max_num):                                      ##3example
    """Генератор, возвращающий четные числа от 0 до max_num."""
    num = 0
    while num <= max_num:
        if num % 2 == 0:
            yield num  # Функция "засыпает", сохраняя состояние
        num += 1

# Создаем генератор
even_gen = even_numbers_up_to(10)

# Итерируемся по значениям
print("Четные числа до 10:")
for value in even_gen:
    print(value, end=" ") # Вывод: 0 2 4 6 8 10

# Списочное включение (создает сразу весь список)
squares_list = [x**2 for x in range(1, 6)]                             #4example
print(f"Список: {squares_list}")      # Вывод: [1, 4, 9, 16, 25]
print(f"Размер в памяти: {squares_list.__sizeof__()} байт")

# Генераторное выражение (создает генератор)
squares_gen = (x**2 for x in range(1, 6))
print(f"\nТип объекта: {type(squares_gen)}") # <class 'generator'>

# Распечатываем значения из генератора
print("Квадраты чисел от 1 до 5:")
for num in squares_gen:
    print(num, end=" ") # Вывод: 1 4 9 16 25

print(f"\nРазмер в памяти: {squares_gen.__sizeof__()} байт") # Обычно меньше, чем у списка