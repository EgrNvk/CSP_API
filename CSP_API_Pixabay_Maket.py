import tkinter as tk
from io import BytesIO

import requests
from PIL import Image, ImageTk

from config import API_KEY


root = tk.Tk()
root.title("Pixabay Maket")
root.geometry("800x700")

photos = []
big_photo = None


def show_big(image_url):
    global big_photo

    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    image.thumbnail((780, 450))

    big_photo = ImageTk.PhotoImage(image)
    big_label.config(image=big_photo)


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

    for widget in thumbs_frame.winfo_children():
        widget.destroy()

    photos.clear()

    image_urls = [item["webformatURL"] for item in data["hits"]]

    if image_urls:
        show_big(image_urls[0])

    for i, image_url in enumerate(image_urls):
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        image.thumbnail((150, 100))

        photo = ImageTk.PhotoImage(image)
        photos.append(photo)

        label = tk.Label(thumbs_frame, image=photo)
        label.grid(row=0, column=i, padx=10, pady=10)

        label.bind("<Button-1>", lambda event, url=image_url: show_big(url))


button = tk.Button(root, text="МІСТО", command=load_images)
button.pack(pady=10)

big_label = tk.Label(root)
big_label.pack(pady=10)

canvas = tk.Canvas(root, height=140)
scrollbar = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)

thumbs_frame = tk.Frame(canvas)

thumbs_frame.bind(
    "<Configure>",
    lambda event: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=thumbs_frame, anchor="nw")
canvas.configure(xscrollcommand=scrollbar.set)

canvas.pack(fill="x")
scrollbar.pack(fill="x")

root.mainloop()