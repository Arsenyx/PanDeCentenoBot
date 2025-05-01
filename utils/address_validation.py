import requests

def validate_address(address: str) -> bool:
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json", "addressdetails": 1, "limit": 1}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if not data:
            return False
        city = data[0].get("address", {}).get("city", "").lower()
        return city in ["valencia", "valència"]
    except Exception as e:
        print(f"Error validating address: {e}")
        return False

# Добавляем заглушку для get_phone
def get_phone(text: str) -> str:
    # Пример простой очистки телефона от пробелов и символов
    return ''.join(filter(str.isdigit, text))

# Добавляем список методов оплаты
payment_method = ['cash', 'card']
