import tkinter as tk
from io import BytesIO

import requests
from PIL import Image, ImageTk

from config import NASA_API_KEY


root = tk.Tk()
root.title("NASA")
root.geometry("900x750")

photos = []
big_photo = None


def show_big(image_url):
    global big_photo

    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    image.thumbnail((850, 450))

    big_photo = ImageTk.PhotoImage(image)
    big_label.config(image=big_photo)


def load_images():
    response = requests.get(
        "https://api.nasa.gov/planetary/apod",
        params={
            "api_key": NASA_API_KEY,
            "start_date": start_entry.get(),
            "end_date": end_entry.get()
        }
    )

    data = response.json()

    for widget in thumbs_frame.winfo_children():
        widget.destroy()

    photos.clear()

    image_urls = []

    for item in data:
        if item["media_type"] == "image":
            image_urls.append(item["url"])

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


top_frame = tk.Frame(root)
top_frame.pack(pady=10)

tk.Label(top_frame, text="Початкова дата:").grid(row=0, column=0, padx=5)
start_entry = tk.Entry(top_frame)
start_entry.grid(row=0, column=1, padx=5)
start_entry.insert(0, "2024-01-01")

tk.Label(top_frame, text="Кінцева дата:").grid(row=0, column=2, padx=5)
end_entry = tk.Entry(top_frame)
end_entry.grid(row=0, column=3, padx=5)
end_entry.insert(0, "2024-01-10")

button = tk.Button(root, text="ЗАВАНТАЖИТИ", command=load_images)
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