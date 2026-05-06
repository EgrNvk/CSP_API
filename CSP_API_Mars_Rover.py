import tkinter as tk
from io import BytesIO

import requests
from PIL import Image, ImageTk

from config import MARS_VISTA_API_KEY


root = tk.Tk()
root.title("Mars Vista")
root.geometry("900x750")

selected_rover = ""
selected_camera = ""

photos = []
big_photo = None
big_label = None
thumbs_frame = None


rovers = {
    "curiosity": ["FHAZ", "RHAZ", "MAST", "CHEMCAM", "MAHLI", "MARDI", "NAVCAM"],
    "opportunity": ["FHAZ", "RHAZ", "NAVCAM", "PANCAM", "MINITES"],
    "spirit": ["FHAZ", "RHAZ", "NAVCAM", "PANCAM", "MINITES"],
    "perseverance": ["EDL_RUCAM", "EDL_RDCAM", "NAVCAM_LEFT", "NAVCAM_RIGHT", "MCZ_RIGHT", "MCZ_LEFT"]
}


def clear():
    for widget in root.winfo_children():
        widget.destroy()


def nav_buttons(back_command=None):
    frame = tk.Frame(root)
    frame.pack(pady=10)

    tk.Button(frame, text="ДОДОМУ", command=show_rovers).grid(row=0, column=0, padx=10)

    if back_command:
        tk.Button(frame, text="НАЗАД", command=back_command).grid(row=0, column=1, padx=10)


def show_rovers():
    clear()

    tk.Label(root, text="Вибери марсохід", font=("Arial", 18)).pack(pady=20)

    for rover in rovers:
        tk.Button(
            root,
            text=rover.upper(),
            width=25,
            command=lambda r=rover: select_rover(r)
        ).pack(pady=5)


def select_rover(rover):
    global selected_rover

    selected_rover = rover
    show_cameras()


def show_cameras():
    clear()
    nav_buttons(show_rovers)

    tk.Label(root, text=f"Марсохід: {selected_rover.upper()}", font=("Arial", 16)).pack(pady=10)
    tk.Label(root, text="Вибери камеру", font=("Arial", 18)).pack(pady=10)

    for camera in rovers[selected_rover]:
        tk.Button(
            root,
            text=camera,
            width=25,
            command=lambda c=camera: select_camera(c)
        ).pack(pady=5)


def select_camera(camera):
    global selected_camera

    selected_camera = camera
    show_dates()


def show_dates():
    clear()
    nav_buttons(show_cameras)

    tk.Label(root, text=f"Марсохід: {selected_rover.upper()}", font=("Arial", 14)).pack(pady=5)
    tk.Label(root, text=f"Камера: {selected_camera}", font=("Arial", 14)).pack(pady=5)

    tk.Label(root, text="Початкова дата YYYY-MM-DD").pack(pady=5)
    start_entry = tk.Entry(root)
    start_entry.pack()
    start_entry.insert(0, "2026-05-01")

    tk.Label(root, text="Кінцева дата YYYY-MM-DD").pack(pady=5)
    end_entry = tk.Entry(root)
    end_entry.pack()
    end_entry.insert(0, "2026-05-06")

    tk.Button(
        root,
        text="ПОКАЗАТИ ГАЛЕРЕЮ",
        command=lambda: show_gallery(start_entry.get(), end_entry.get())
    ).pack(pady=20)


def get_photos_from_response(data):
    return data["data"]


def get_image_url(item):
    return item["attributes"]["images"]["full"]


def show_big(image_url):
    global big_photo

    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    image.thumbnail((850, 450))

    big_photo = ImageTk.PhotoImage(image)
    big_label.config(image=big_photo, text="")


def load_images(start_date, end_date):
    response = requests.get(
        "https://api.marsvista.dev/api/v2/photos",
        headers={
            "X-API-Key": MARS_VISTA_API_KEY
        },
        params={
            "rovers": selected_rover,
            "cameras": selected_camera,
            "earth_date_min": start_date,
            "earth_date_max": end_date,
            "page_size": 30
        }
    )

    print(response.url)
    print(response.status_code)
    print(response.text[:500])

    if response.status_code != 200:
        big_label.config(text="Помилка запиту до Mars Vista API")
        return []

    data = response.json()
    items = get_photos_from_response(data)

    image_urls = []

    for item in items:
        url = get_image_url(item)

        if url:
            image_urls.append(url)

    return image_urls


def show_gallery(start_date, end_date):
    global big_label
    global thumbs_frame

    clear()
    nav_buttons(show_dates)

    tk.Label(
        root,
        text=f"{selected_rover.upper()} | {selected_camera} | {start_date} - {end_date}",
        font=("Arial", 14)
    ).pack(pady=5)

    big_label = tk.Label(root)
    big_label.pack(pady=10)

    canvas = tk.Canvas(root, height=150)
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

    photos.clear()

    image_urls = load_images(start_date, end_date)

    if not image_urls:
        big_label.config(text="Фото не знайдено")
        return

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


show_rovers()
root.mainloop()