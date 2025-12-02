# main.py

import customtkinter as ctk
# Import kelas utama aplikasi dari modul app_ui
from modules.app_ui import ResepApp

# --- KONFIGURASI DAN JALANKAN APLIKASI ---

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

if __name__ == "__main__":
    app = ResepApp()
    app.mainloop()