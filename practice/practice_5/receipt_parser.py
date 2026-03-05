import re
import json
from datetime import datetime

def extract_prices(text):
    """Extract all prices from the receipt"""
    prices = re.findall(r'(\d+(?:[ \d]+)?,\d{2})', text)
    return [float(price.replace(' ', '').replace(',', '.')) for price in prices]

def find_product_names(text):
    """Find all product names from the receipt"""
    products = []
    lines = text.split('\n')
    
    for line in lines:
        if re.match(r'\d+\.', line) and 'x' not in line and 'Стоимость' not in line:
            # Убираем номер и точку в начале
            product = re.sub(r'^\d+\.\s*', '', line)
            # Убираем [RX]- если есть
            product = re.sub(r'\[RX\]-', '', product)
            products.append(product.strip())
    
    return products

def calculate_total(text):
    """Calculate total amount from receipt"""
    match = re.search(r'ИТОГО:\s*(\d+(?:[ \d]+)?,\d{2})', text)
    if match:
        total_str = match.group(1).replace(' ', '').replace(',', '.')
        return float(total_str)
    
    # Если не нашли ИТОГО, суммируем все стоимости
    costs = re.findall(r'Стоимость\s*(\d+(?:[ \d]+)?,\d{2})', text)
    total = 0
    for cost in costs:
        total += float(cost.replace(' ', '').replace(',', '.'))
    return total

def extract_datetime(text):
    """Extract date and time information from receipt"""
    match = re.search(r'Время:\s*(\d{2}\.\d{2}\.\d{4}\s*\d{2}:\d{2}:\d{2})', text)
    if match:
        return match.group(1)
    return "Not found"

def find_payment_method(text):
    """Find payment method from receipt"""
    if 'Банковская карта' in text:
        return "Bank card"
    elif 'Наличные' in text:
        return "Cash"
    else:
        return "Unknown"

def create_structured_output(prices, products, total, datetime_str, payment_method):
    """Create structured output (JSON or formatted text)"""
    
    # Создаем структуру данных
    output = {
        "receipt_data": {
            "date_time": datetime_str,
            "payment_method": payment_method,
            "total_amount": total,
            "number_of_products": len(products),
            "products": products,
            "all_prices": prices
        },
        "summary": {
            "min_price": min(prices) if prices else 0,
            "max_price": max(prices) if prices else 0,
            "avg_price": round(sum(prices)/len(prices), 2) if prices else 0
        }
    }
    
    return output

def main():
    # Читаем файл с чеком
    try:
        with open('raw.txt', 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        print("Error: raw.txt file not found!")
        return
    
    # Выполняем все задачи
    print("=" * 60)
    print("RECEIPT PARSING RESULTS")
    print("=" * 60)
    
    # 1. Extract all prices
    prices = extract_prices(text)
    print(f"\n1. ALL PRICES ({len(prices)} prices):")
    print("-" * 40)
    # Показываем все цены
    for i, price in enumerate(prices, 1):
        print(f"   Price {i:2d}: {price:8.2f}")
    
    # 2. Find all product names
    products = find_product_names(text)
    print(f"\n2. ALL PRODUCT NAMES ({len(products)} products):")
    print("-" * 40)
    for i, product in enumerate(products, 1):
        print(f"   {i:2d}. {product}")
    
    # 3. Calculate total amount
    total = calculate_total(text)
    print(f"\n3. TOTAL AMOUNT:")
    print("-" * 40)
    print(f"   Total: {total:.2f}")
    
    # 4. Extract date and time
    datetime_str = extract_datetime(text)
    print(f"\n4. DATE AND TIME:")
    print("-" * 40)
    print(f"   {datetime_str}")
    
    # 5. Find payment method
    payment_method = find_payment_method(text)
    print(f"\n5. PAYMENT METHOD:")
    print("-" * 40)
    print(f"   {payment_method}")
    
    # 6. Create structured output
    print(f"\n6. STRUCTURED OUTPUT (JSON format):")
    print("-" * 40)
    
    output_data = create_structured_output(prices, products, total, datetime_str, payment_method)
    
    # Выводим JSON
    json_output = json.dumps(output_data, ensure_ascii=False, indent=2)
    print(json_output)
    
    # Сохраняем в файл
    with open('parsed_receipt.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Results saved to parsed_receipt.json")
    print("=" * 60)

if __name__ == "__main__":
    main()