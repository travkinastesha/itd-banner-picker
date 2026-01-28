import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import requests, os, time
from io import BytesIO

import sv_ttk

# --- Настройки ---

TARGET_SIZE = (320, 107)
API_UPLOAD_URL = "https://xn--d1ah4a.com/api/files/upload"
API_UPDATE_URL = "https://xn--d1ah4a.com/api/users/me"
TOKEN = ""

# --- API функции ---
def resize_image(path_to_image: str, target_size=TARGET_SIZE):
    img = Image.open(path_to_image)
    buffer = BytesIO()
    
    new_w = target_size[0]
    new_h = int(target_size[1] * (target_size[0] / img.size[0]))
    if new_h < 107:
        new_h = int(target_size[1] * (img.size[0] / target_size[0]))
    size = (new_w, new_h)
    print(size)
    img = img.resize(size, Image.LANCZOS)
    
    if not path_to_image.lower().endswith(".gif"):
        img.save(buffer, format="PNG")
        buffer.name = f"banner-{int(time.time() * 1000)}.png"
        buffer.seek(0)
    else:
        with open(path_to_image, "rb") as f:
            name = f"banner-{int(time.time() * 1000)}.gif"
            data = f.read()
            buffer = BytesIO(data)
            buffer.name = name
            
    return buffer

def upload_image(path_to_image):
    global TOKEN
    if not TOKEN:
        messagebox.showerror("Error", "Введите токен!")
        return
    if not os.path.exists(path_to_image):
        messagebox.showerror("Error", "Файл не найден")
        return

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "*/*",
        "Origin": "https://xn--d1ah4a.com",
        "Referer": "https://xn--d1ah4a.com",
        "User-Agent": "Mozilla/5.0",
    }

    buffer = resize_image(path_to_image)
    files = {"file": buffer}

    try:
        response = requests.post(API_UPLOAD_URL, headers=headers, files=files)
        if response.status_code == 200 or response.status_code == 201:
            json_resp = response.json()
            bannerID = json_resp.get("id")
            if bannerID:
                update_banner(bannerID)
                messagebox.showinfo("Success", "Баннер успешно обновлён!")
            else:
                messagebox.showerror("Error", "Не удалось получить ID баннера")
        else:
            messagebox.showerror("Error", f"Upload failed: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_banner(bannerID: str):
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "*/*",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
    }
    data = {"bannerId": bannerID}
    response = requests.put(API_UPDATE_URL, headers=headers, json=data)
    print("Update Status:", response.status_code)
    try:
        print("Update Response JSON:", response.json())
    except:
        print("Response text:", response.text)

# --- GUI функции ---
def select_file():
    #file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")])
    file_path = filedialog.askopenfilename()
    if file_path:
        load_preview(file_path)

def load_preview(file_path, target_size=TARGET_SIZE):
    img = Image.open(file_path)
    
    # Изменяем размер изображения, сохраняя пропорции
    new_w = target_size[0]
    new_h = int(target_size[1] * (target_size[0] / img.size[0]))
    if new_h < 107:
        new_h = int(target_size[1] * (img.size[0] / target_size[0]))
    size = (new_w, new_h)
    print(size)
    img = img.resize(size, Image.LANCZOS)
    
    img_tk = ImageTk.PhotoImage(img)
    
    preview_label.configure(image=img_tk)
    preview_label.image = img_tk
    preview_label.file_path = file_path

def on_upload():
    global TOKEN
    TOKEN = token_entry.get().strip()
    if hasattr(preview_label, 'file_path'):
        upload_image(preview_label.file_path)
    else:
        messagebox.showerror("Error", "Выберите файл для загрузки!")

# --- Главное окно ---
root = ctk.CTk()
root.title("ITD banner picker")
root.geometry("450х350")
root.resizable(False, False)

# --- Поле для токена с Bearer ---
token_frame = ctk.CTkFrame(root, corner_radius=10, fg_color="#2e2e2e")
token_frame.pack(pady=(20, 20), padx=20, fill="x")

bearer_label = ctk.CTkLabel(token_frame, text="Bearer", width=50, anchor="w", corner_radius=10)
bearer_label.pack(side="left", padx=(0,0), pady=5)

token_entry = ctk.CTkEntry(token_frame, placeholder_text="Твой токен должен быть тут")
token_entry.pack(side="left", fill="x", expand=True, padx=(0,5), pady=5)

# --- Бокс баннера ---
banner_frame = ctk.CTkFrame(root, width=TARGET_SIZE[0], height=TARGET_SIZE[1], corner_radius=0)
banner_frame.pack(pady=10)
banner_frame.pack_propagate(False)
banner_label = ctk.CTkLabel(banner_frame, text="Кликни чтобы выбрать баннер\nРекомендуемый размер: 320x107")
banner_label.pack(expand=True)

preview_label = ctk.CTkLabel(banner_frame, text="")
preview_label.place(relx=0.5, rely=0.5, anchor="center")

banner_frame.bind("<Button-1>", lambda e: select_file())
banner_label.bind("<Button-1>", lambda e: select_file())
preview_label.bind("<Button-1>", lambda e: select_file())

# --- Кнопка загрузки (закруглённая) ---
upload_btn = ctk.CTkButton(root, text="Установить баннер", corner_radius=10, command=on_upload, width=TARGET_SIZE[0]-40,)
upload_btn.pack(pady=20)

credit_label = ctk.CTkLabel(root, text="c <3 от @travkinastesha на GitHub и ИТД", width=TARGET_SIZE[0]-40,)
credit_label.pack(pady=(0,20))

root.mainloop()