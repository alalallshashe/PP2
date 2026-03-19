import re
import json

def parse_receipt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return {"error": f"Файл '{file_path}' не найден"}

    # 1. Извлечение даты и времени
    dt_match = re.search(r'Время:\s*([\d.]+ \d{2}:\d{2}:\d{2})', content)
    date_time = dt_match.group(1) if dt_match else "Не найдено"

    # 2. Определение метода оплаты
    payment_method = "Карта" if "Банковская карта" in content else "Наличные"

    # 3. Извлечение ИТОГО
    total_match = re.search(r'ИТОГО:\s*([\d\s]+,\d{2})', content)
    total_val = 0.0
    if total_match:
        total_val = float(total_match.group(1).replace(' ', '').replace(',', '.'))

    # 4. Разбор товаров
    products = []
    items = re.split(r'\n\s*(\d+)\.\n', content)
    
    # Список слов, на которых нужно остановить сбор названия
    stop_words = ["Стоимость", "Банковская карта", "Наличные", "в т.ч. НДС", "Фискальный", "Время"]

    for i in range(2, len(items), 2):
        block = items[i]
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        
        name_parts = []
        quantity = 0.0
        unit_price = 0.0
        
        for line in lines:
            # Ищем строку с количеством и ценой (X)
            calc_match = re.search(r'([\d\s,]+)\s*x\s*([\d\s,]+)', line)
            if calc_match:
                quantity = float(calc_match.group(1).replace(' ', '').replace(',', '.'))
                unit_price = float(calc_match.group(2).replace(' ', '').replace(',', '.'))
                continue # Переходим к следующей строке
            
            # Проверяем, не является ли строка началом подвала чека
            if any(stop in line for stop in stop_words):
                # Если нашли стоп-слово, обрезаем строку до него и выходим из цикла для этого товара
                for stop in stop_words:
                    if stop in line:
                        clean_part = line.split(stop)[0].strip()
                        if clean_part: name_parts.append(clean_part)
                break 

            # Обычная очистка строки названия
            clean_line = line.replace('[RX]-', '').strip()
            if clean_line:
                name_parts.append(clean_line)

        full_name = " ".join(name_parts).strip()
        if full_name or unit_price > 0:
            products.append({
                "name": full_name,
                "quantity": quantity,
                "unit_price": unit_price,
                "total_item": round(quantity * unit_price, 2)
            })

    return {
        "info": {
            "date": date_time,
            "payment": payment_method,
            "total_sum": total_val
        },
        "products": products
    }

if __name__ == "__main__":
    input_file = 'raw.txt'
    output_file = 'receipt.json'
    
    data = parse_receipt(input_file)
    
    if "error" not in data:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        # Вывод в терминал
        print("\n=== ДАННЫЕ ИЗ ЧЕКА ===")
        print(json.dumps(data, ensure_ascii=False, indent=4))
        print("======================\n")
    else:
        print(f"Ошибка: {data['error']}")