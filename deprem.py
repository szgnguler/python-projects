import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests

def get_latest_earthquakes():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
    response = requests.get(url)
    data = response.json()
    earthquakes = data["features"]
    return earthquakes

def display_latest_earthquakes():
    earthquakes = get_latest_earthquakes()[:50]
    
    # Tabloyu temizle
    for row in tree.get_children():
        tree.delete(row)
    
    # Depremleri tabloya ekle
    for quake in earthquakes:
        place = quake['properties']['place']
        mag = quake['properties']['mag']
        tree.insert("", "end", values=(place, mag))

def check_for_new_earthquake():
    global previous_earthquakes
    latest_earthquakes = get_latest_earthquakes()
    if latest_earthquakes != previous_earthquakes:
        messagebox.showinfo("Yeni Deprem!", "Yeni bir deprem meydana geldi!")
    else:
        messagebox.showinfo("Yeni Deprem Yok", "Yeni bir deprem meydana gelmedi.")
    previous_earthquakes = latest_earthquakes

def about():
    about_window = tk.Toplevel(root)
    about_window.title("Hakkında")
    about_window.geometry("300x100")
    about_label = ttk.Label(about_window, text="Tasarım & Sezgin Güler", font=("Arial", 12))
    about_label.pack(padx=10, pady=10)

def select_and_highlight(event):
    item = tree.selection()[0]
    tree.tag_configure("bold", font=("Arial", 10, "bold"))
    tree.item(item, tags=("bold",))

root = tk.Tk()
root.title("Son Depremler")
root.geometry("600x400")

# Tablo oluştur
tree = ttk.Treeview(root, columns=("Place", "Magnitude"), show="headings")
tree.heading("Place", text="Yer")
tree.heading("Magnitude", text="Büyüklük")
tree.pack(fill="both", expand=True)

# Butonları oluştur
button_frame = ttk.Frame(root)
button_frame.pack(fill="x")

get_earthquakes_button = ttk.Button(button_frame, text="Son Depremleri Getir", command=display_latest_earthquakes)
get_earthquakes_button.pack(side="left", padx=5, pady=5)

check_button = ttk.Button(button_frame, text="Yeni Depremi Kontrol Et", command=check_for_new_earthquake)
check_button.pack(side="left", padx=5, pady=5)

close_button = ttk.Button(button_frame, text="Kapat", command=root.destroy)
close_button.pack(side="left", padx=5, pady=5)

# Hakkında sekmesi
about_button = ttk.Button(button_frame, text="Hakkında", command=about)
about_button.pack(side="left", padx=5, pady=5)

# Türkiye'deki depremleri seçmek için olay ekle
tree.bind("<<TreeviewSelect>>", select_and_highlight)

previous_earthquakes = get_latest_earthquakes()  # Önceki depremleri al

root.mainloop()
