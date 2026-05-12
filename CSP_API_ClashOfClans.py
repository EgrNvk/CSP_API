import tkinter as tk
from tkinter import ttk
import requests
from config import COC_API_KEY

BASE = "https://api.clashofclans.com/v1"
HEADERS = {"Authorization": f"Bearer {COC_API_KEY}"}

cursor_after = None
history = []

def load_countries():
    data = requests.get(f"{BASE}/locations", headers=HEADERS, params={"limit": 500}, timeout=10).json()
    countries = [loc for loc in data.get("items", []) if loc.get("isCountry")]
    countries.sort(key=lambda x: x["name"])
    print(countries)
    return countries

def top20(after=None):
    global cursor_after, history
    if after is None:
        history.clear()

    selected = combo.get()
    country = next((c for c in countries if c["name"] == selected), None)
    if not country:
        return

    params = {"limit": 20}
    if after:
        params["after"] = after

    url = f"{BASE}/locations/{country['id']}/rankings/players"
    data = requests.get(url, headers=HEADERS, params=params, timeout=10).json()
    print(data)

    cursor_after = data.get("paging", {}).get("cursors", {}).get("after")

    for row in tree.get_children():
        tree.delete(row)

    offset = len(history) * 20
    for i, p in enumerate(data.get("items", []), 1 + offset):
        tree.insert("", "end", values=(
            i,
            p.get("name", "—"),
            p.get("trophies", 0),
            p.get("clan", {}).get("name", "—"),
        ))

    btn_next.config(state="normal" if cursor_after else "disabled")
    btn_prev.config(state="normal" if history else "disabled")

def next20():
    history.append(cursor_after)
    top20(after=cursor_after)

def prev20():
    history.pop()
    top20(after=history[-1] if history else None)

root = tk.Tk()
root.title("CoC — Топ гравці")
root.geometry("640x540")

top = tk.Frame(root, pady=10)
top.pack(fill="x", padx=10)

tk.Label(top, text="Країна:").pack(side="left")

countries = load_countries()
names = [c["name"] for c in countries]

combo = ttk.Combobox(top, values=names, width=24, state="readonly")
combo.set("Ukraine")
combo.pack(side="left", padx=8)

tk.Button(top, text="Топ-20", command=top20, padx=10).pack(side="left")

cols = ("#", "Ім'я", "Трофеї", "Клан")
tree = ttk.Treeview(root, columns=cols, show="headings", height=20)
for col, w in zip(cols, [40, 160, 90, 180]):
    tree.heading(col, text=col)
    tree.column(col, width=w, anchor="center")
tree.column("Ім'я", anchor="w")
tree.column("Клан", anchor="w")
tree.pack(fill="both", expand=True, padx=10, pady=(0, 6))

nav = tk.Frame(root, pady=6)
nav.pack()

btn_prev = tk.Button(nav, text="← Попередні 20", command=prev20, padx=10, state="disabled")
btn_prev.pack(side="left", padx=6)

btn_next = tk.Button(nav, text="Наступні 20 →", command=next20, padx=10, state="disabled")
btn_next.pack(side="left", padx=6)

root.mainloop()