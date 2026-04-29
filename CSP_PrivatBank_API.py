# [
#         {
#         "ccy":"EUR",
#         "base_ccy":"UAH",
#         "buy":"19.20000",
#         "sale":"20.00000"
#         },
#         {
#         "ccy":"USD",
#         "base_ccy":"UAH",
#         "buy":"15.50000",
#         "sale":"15.85000"
#         }
# ]
import requests

currency_name = input("Введіть валюту (наприклад USD, EUR): ").upper()

url = "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5"

try:
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    for currency in data:
        if currency["ccy"] == currency_name:
            print(f"\nКурс для {currency_name}: Купівля: {currency['buy']} Продаж: {currency['sale']}")
            break
    else:
        print("Таку валюту не знайдено.")

except requests.exceptions.RequestException as e:
    print("Помилка при отриманні курсу валют:", e)