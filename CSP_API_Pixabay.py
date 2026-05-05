import tkinter as tk
from io import BytesIO

import requests
from PIL import Image, ImageTk

from config import API_KEY


root = tk.Tk()
root.title("Pixabay")
root.geometry("800x600")

photos = []


def load_images():
    response = requests.get(
        "https://pixabay.com/api/",
        params={
            "key": API_KEY,
            "q": "city",
            "image_type": "photo",
            "per_page": 30
        }
    )

    data = response.json()

    for widget in gallery.winfo_children():
        widget.destroy()

    photos.clear()

    for i, item in enumerate(data["hits"]):
        image_url = item["webformatURL"]

        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image_response.content))
        image.thumbnail((250, 180))

        photo = ImageTk.PhotoImage(image)
        photos.append(photo)

        label = tk.Label(gallery, image=photo)

        row = i // 3
        col = i % 3

        label.grid(row=row, column=col, padx=5, pady=5)


button = tk.Button(root, text="МІСТО", command=load_images)
button.pack(pady=10)

canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, command=canvas.yview)
gallery = tk.Frame(canvas)

gallery.bind(
    "<Configure>",
    lambda event: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=gallery, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

root.mainloop()