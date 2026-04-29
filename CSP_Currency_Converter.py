import tkinter as tk
import requests


url = "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5"

response = requests.get(url)
data = response.json()

print("Запит")
print(url)
print("Статус")
print(response.status_code)
print("Відповідь")
print(response.text)

rates = {"UAH": 1}

for i in data:
    rates[i["ccy"]] = float(i["sale"])


def convert(*args):
    try:
        amount = float(entry.get())
        from_currency = from_var.get()
        to_currency = to_var.get()
        result = amount * rates[from_currency] / rates[to_currency]
        result_label.config(
            text=f"Результат: {round(result, 2)} {to_currency}"
        )
    except:
        result_label.config(text="Введіть суму")

root = tk.Tk()
root.title("Конвертер валют")
root.geometry("300x200")

tk.Label(root, text="Сума").pack()

entry = tk.Entry(root)
entry.pack()
entry.bind("<KeyRelease>", convert)

from_var = tk.StringVar()
from_var.set("UAH")

tk.OptionMenu(root, from_var, *rates.keys(), command=convert).pack()

to_var = tk.StringVar()
to_var.set("USD")

tk.OptionMenu(root, to_var, *rates.keys(), command=convert).pack()

result_label = tk.Label(root, text="Результат")
result_label.pack(pady=20)

root.mainloop()