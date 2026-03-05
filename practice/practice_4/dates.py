from datetime import date, time, datetime, timedelta  #1example

# Создание объектов даты
current_date = date.today()  # Текущая дата
print(f"Текущая дата: {current_date}")
print(f"Год: {current_date.year}, Месяц: {current_date.month}, День: {current_date.day}")

# Создание произвольной даты
birth_date = date(1995, 5, 15)
print(f"\nДата рождения: {birth_date}")
print(f"День недели (0=пн, 6=вс): {birth_date.weekday()}")  # Понедельник=0

# Создание объектов времени
meeting_time = time(14, 30, 45)  # 14:30:45
print(f"\nВремя встречи: {meeting_time}")
print(f"Часы: {meeting_time.hour}, Минуты: {meeting_time.minute}")

# Комбинированный объект datetime
now = datetime.now()  # Текущие дата и время
print(f"\nТекущий момент: {now}")
print(f"Микросекунды: {now.microsecond}")

from datetime import datetime  ##2example

# Получаем текущее время
now = datetime.now()

# Форматирование даты в строку (datetime -> str)
formats = [
    "%d.%m.%Y",                    # 26.02.2026
    "%d %B %Y года",               # 26 февраля 2026 года
    "%A, %d %B %Y %H:%M",          # Thursday, 26 February 2026 15:30
    "%Y-%m-%d %H:%M:%S",           # 2026-02-26 15:30:45
    "%I:%M %p",                    # 03:30 PM
]

print("Различные форматы текущей даты:")
for fmt in formats:
    print(f"  {fmt}: {now.strftime(fmt)}")

# Парсинг строки в дату (str -> datetime)
date_string = "15 мая 2025 14:30"
parsed_date = datetime.strptime(date_string, "%d %B %Y %H:%M")
print(f"\nРаспарсенная дата: {parsed_date}")
print(f"Тип объекта: {type(parsed_date)}")

from datetime import datetime, timedelta, date ##3example

# Разница между двумя датами
start_date = date(2025, 1, 1)
end_date = date(2026, 2, 26)
delta = end_date - start_date
print(f"Дней между {start_date} и {end_date}: {delta.days}")

# Арифметика с датами
today = date.today()
print(f"\nСегодня: {today}")

# Добавление и вычитание времени
one_week_later = today + timedelta(weeks=1)
print(f"Через неделю: {one_week_later}")

three_days_ago = today - timedelta(days=3)
print(f"3 дня назад: {three_days_ago}")

two_months_later = today + timedelta(days=60)  # Приблизительно 2 месяца
print(f"Через ~2 месяца: {two_months_later}")

# Разница во времени с точностью до секунд
start_time = datetime.now()
# Имитация выполнения операции
import time
time.sleep(2.5)
end_time = datetime.now()

execution_time = end_time - start_time
print(f"\nВремя выполнения: {execution_time.total_seconds():.2f} секунд")
print(f"Точное значение: {execution_time}")

from datetime import datetime ##4example
import pytz

# Получение списка всех часовых поясов
print("Доступные часовые пояса (первые 5):")
all_timezones = pytz.all_timezones[:5]
for tz in all_timezones:
    print(f"  {tz}")

# Текущее время в UTC
utc_now = datetime.now(pytz.UTC)
print(f"\nВремя UTC: {utc_now.strftime('%Y-%m-%d %H:%M:%S %Z')}")

# Конвертация в разные часовые пояса
timezones_to_check = [
    'Europe/Moscow',
    'Europe/London',
    'America/New_York',
    'Asia/Tokyo',
    'Australia/Sydney'
]

print("\nТекущее время в разных городах:")
for tz_name in timezones_to_check:
    tz = pytz.timezone(tz_name)
    local_time = utc_now.astimezone(tz)
    print(f"  {tz_name:20}: {local_time.strftime('%Y-%m-%d %H:%M:%S')}")

# Создание даты с конкретным часовым поясом
moscow_tz = pytz.timezone('Europe/Moscow')
moscow_time = moscow_tz.localize(datetime(2025, 12, 31, 23, 59, 59))
print(f"\nНовый год в Москве: {moscow_time}")
print(f"В UTC это будет: {moscow_time.astimezone(pytz.UTC)}")

# Важное замечание о timedelta с timezone-aware объектами
print(f"\nСмещение московского времени: {moscow_time.utcoffset()}")
print(f"Название зоны: {moscow_time.tzname()}")