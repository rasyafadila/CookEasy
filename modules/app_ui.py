import customtkinter as ctk
import json
import os
from PIL import Image, ImageTk
# --- KONFIGURASI DAN DATA ---
DATA_FILE = 'data/resep.json'
ctk.set_appearance_mode("System")  # Pilihan: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")
print("hello world")
# --- HANDLER JSON ---
def muat_resep():
    """Memuat data resep dari file JSON. Mengembalikan list kosong jika gagal."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def simpan_resep(resep_list):
    """Menyimpan data resep ke file JSON."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(resep_list, f, indent=2)

# --- KELAS UTAMA APLIKASI ---
class ResepApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Konfigurasi Jendela
        self.title("🍲 Aplikasi Resep Masakan")
        self.geometry("1000x700")
        self.resep_data = muat_resep() 
        
        # Grid Utama (1: Navigasi, 2: Konten)
        self.grid_columnconfigure(0, weight=0) # Sidebar
        self.grid_columnconfigure(1, weight=1) # Konten
        self.grid_rowconfigure(0, weight=1)
        
        self.current_frame = None # Untuk melacak frame yang sedang ditampilkan

        # Panggil Setup UI
        self._setup_sidebar()
        
        # Tampilkan Halaman Awal
        self.show_frame("daftar")

    def _setup_sidebar(self):
        """Membuat sidebar navigasi yang statis."""
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        ctk.CTkLabel(self.sidebar_frame, text="RESEP MASAKAN", 
                     font=ctk.CTkFont(size=22, weight="bold")).grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Tombol Navigasi
        ctk.CTkButton(self.sidebar_frame, text="❓ Masak Apa Hari Ini?", 
                      command=lambda: self.show_frame("saran")).grid(row=1, column=0, padx=20, pady=10, sticky="ew") 
        
        ctk.CTkButton(self.sidebar_frame, text="📚 Daftar Resep", 
                      command=lambda: self.show_frame("daftar")).grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        ctk.CTkButton(self.sidebar_frame, text="➕ Tambah Resep", 
                      command=lambda: self.show_frame("tambah")).grid(row=3, column=0, padx=20, pady=10, sticky="ew") 
        
        # Dropdown untuk Mode Tampilan
        appearance_label = ctk.CTkLabel(self.sidebar_frame, text="Mode Tampilan:", anchor="w")
        appearance_label.grid(row=5, column=0, padx=20, pady=(10, 0), sticky="s")
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                             command=ctk.set_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(0, 20), sticky="s")
        self.appearance_mode_optionemenu.set("System")
        
    def show_frame(self, name, resep_id=None):
        """Menghapus frame lama dan menampilkan frame baru."""
        if self.current_frame:
            self.current_frame.destroy()

        if name == "daftar":
            self.current_frame = DaftarResepFrame(self)
        elif name == "tambah":
            self.current_frame = FormTambahResepFrame(self)
        elif name == "detail" and resep_id is not None:
            resep = next((r for r in self.resep_data if r['id'] == resep_id), None)
            if resep:
                 self.current_frame = DetailResepFrame(self, resep)
            else:
                 self.current_frame = ctk.CTkLabel(self, text="Resep tidak ditemukan.")
                 self.current_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
                 return

        self.current_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

#image
class SaranResepFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, label_text="❓ Masak Apa Hari Ini? - Pilihan Best Seller", 
                         label_font=ctk.CTkFont(size=20, weight="bold"))
        self.master = master
        self.grid_columnconfigure(0, weight=1)
        
        self.tampilkan_saran()

    def tampilkan_saran(self):
        
        bestsellers = [r for r in self.master.resep_data if r.get('is_bestseller')]
        
        if not bestsellers:
            ctk.CTkLabel(self, text="Tidak ada resep yang ditandai sebagai Best Seller saat ini.").pack(pady=50)
            return

        for resep in bestsellers:
            # 1. Buat Kartu Kontainer
            card = ctk.CTkFrame(self, fg_color=("gray90", "gray15"))
            card.pack(fill="x", padx=10, pady=10)
            card.grid_columnconfigure(1, weight=1)
            
            directory = os.path.dirname(__file__)                
            gambar_path = os.path.join(directory, 'assets/nasi_goreng.jpg')
            
            # 2. Muat dan Tampilkan Gambar
            if gambar_path and os.path.exists(gambar_path):
                try:
                    # Muat gambar menggunakan PIL dan resize
                    img_pil = Image.open(gambar_path).resize((150, 100)) 
                    img_ctk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(150, 100))
                    
                    # Tampilkan di Label
                    img_label = ctk.CTkLabel(card, text="", image=img_ctk)
                    img_label.grid(row=0, column=0, rowspan=2, padx=15, pady=10, sticky="nsw")
                    
                except Exception as e:
                    print(f"Gagal memuat gambar untuk {resep['nama']}: {e}")
                    ctk.CTkLabel(card, text="[Gambar Gagal Dimuat]").grid(row=0, column=0, rowspan=2, padx=15, pady=10, sticky="nsw")
            else:
                 ctk.CTkLabel(card, text="[Gambar Tidak Tersedia]").grid(row=0, column=0, rowspan=2, padx=15, pady=10, sticky="nsw")

            # 3. Judul Resep
            ctk.CTkLabel(card, text=resep['nama'], font=ctk.CTkFont(size=22, weight="bold"), 
                         anchor="w").grid(row=0, column=1, padx=(5, 15), pady=10, sticky="w")
            
            # 4. Tombol Aksi
            ctk.CTkButton(card, text="Lihat Resep & Masak", 
                          command=lambda r_id=resep['id']: self.master.show_frame("detail", r_id)).grid(row=1, column=1, padx=(5, 15), pady=(0, 10), sticky="w")
# --- KELAS FRAME KONTEN ---

class DaftarResepFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, label_text="Daftar Semua Resep", label_font=ctk.CTkFont(size=20, weight="bold"))
        self.master = master
        self.grid_columnconfigure(0, weight=1)
        self.tampilkan_list_resep()

    def tampilkan_list_resep(self):
        """Membuat kartu-kartu resep di dalam scrollable frame."""
        resep_list = self.master.resep_data
        
        if not resep_list:
            ctk.CTkLabel(self, text="Belum ada resep yang tersimpan. Klik 'Tambah Resep' untuk memulai!",
                         font=ctk.CTkFont(size=16)).pack(pady=50)
            return

        for i, resep in enumerate(resep_list):
            card = ctk.CTkFrame(self, fg_color=("gray80", "gray20"))
            card.pack(fill="x", padx=10, pady=5)
            card.grid_columnconfigure(0, weight=1)
            
            # Judul Resep
            ctk.CTkLabel(card, text=resep['nama'], font=ctk.CTkFont(size=18, weight="bold"), anchor="w").grid(row=0, column=0, padx=15, pady=10, sticky="w")
            
            # Tombol Lihat Detail
            ctk.CTkButton(card, text="Lihat Detail", 
                          command=lambda r_id=resep['id']: self.master.show_frame("detail", r_id)).grid(row=0, column=1, padx=10, pady=10, sticky="e")
            
            # Tombol Hapus (Tambahan Fitur)
            ctk.CTkButton(card, text="🗑️", width=40, fg_color="red", hover_color="darkred", 
                          command=lambda r_id=resep['id'], r_nama=resep['nama']: self.konfirmasi_hapus(r_id, r_nama)).grid(row=0, column=2, padx=(0, 10), pady=10, sticky="e")

    def konfirmasi_hapus(self, resep_id, resep_nama):
        """Menampilkan dialog konfirmasi sebelum menghapus."""
        if ctk.CTkMessagebox.ask_question("Konfirmasi Hapus", 
                                          f"Yakin ingin menghapus resep '{resep_nama}'?", 
                                          icon="warning"):
            self.master.resep_data = [r for r in self.master.resep_data if r['id'] != resep_id]
            simpan_resep(self.master.resep_data)
            self.master.show_frame("daftar") # Muat ulang tampilan


class DetailResepFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, resep):
        super().__init__(master, label_text=f"Detail Resep: {resep['nama']}", label_font=ctk.CTkFont(size=20, weight="bold"))
        self.master = master
        self.resep = resep
        self.grid_columnconfigure(0, weight=1)
        self.display_details()

    def display_details(self):
        """Menampilkan bahan dan langkah memasak."""
        
        # Judul Besar
        ctk.CTkLabel(self, text=self.resep['nama'], font=ctk.CTkFont(size=36, weight="bold")).pack(pady=(10, 20))
        
        # --- Bagian Bahan ---
        bahan_frame = ctk.CTkFrame(self, fg_color=("gray90", "gray10"))
        bahan_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(bahan_frame, text="✅ Bahan-Bahan", font=ctk.CTkFont(size=20, weight="bold"), anchor="w").pack(fill="x", padx=15, pady=(10, 5))
        
        bahan_text = "\n".join([f"• {b}" for b in self.resep['bahan']])
        ctk.CTkLabel(bahan_frame, text=bahan_text, justify="left", anchor="w").pack(fill="x", padx=25, pady=(0, 10))

        # --- Bagian Langkah ---
        langkah_frame = ctk.CTkFrame(self, fg_color=("gray90", "gray10"))
        langkah_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(langkah_frame, text="📝 Langkah Memasak", font=ctk.CTkFont(size=20, weight="bold"), anchor="w").pack(fill="x", padx=15, pady=(10, 5))
        
        langkah_text = "\n".join([f"{i+1}. {l}" for i, l in enumerate(self.resep['langkah'])])
        ctk.CTkLabel(langkah_frame, text=langkah_text, justify="left", anchor="w").pack(fill="x", padx=25, pady=(0, 10))
        
        # Tombol Kembali
        ctk.CTkButton(self, text="⬅️ Kembali ke Daftar", command=lambda: self.master.show_frame("daftar")).pack(pady=30)


class FormTambahResepFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid_columnconfigure(0, weight=1)
        self.create_form()

    def create_form(self):
        ctk.CTkLabel(self, text="➕ Tambah Resep Baru", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=20)
        
        # Container untuk Kontrol
        form_scroll_frame = ctk.CTkScrollableFrame(self)
        form_scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        form_scroll_frame.grid_columnconfigure(0, weight=1)

        # 1. Input Nama Resep
        ctk.CTkLabel(form_scroll_frame, text="Nama Resep:", anchor="w", font=ctk.CTkFont(size=16, weight="bold")).pack(fill="x", padx=15, pady=(10, 0))
        self.entry_nama = ctk.CTkEntry(form_scroll_frame, placeholder_text="Contoh: Ayam Bakar Madu")
        self.entry_nama.pack(fill="x", padx=15, pady=(0, 10))
        
        # 2. Input Bahan
        ctk.CTkLabel(form_scroll_frame, text="Bahan-Bahan (Satu bahan per baris):", anchor="w", font=ctk.CTkFont(size=16, weight="bold")).pack(fill="x", padx=15, pady=(10, 0))
        self.textbox_bahan = ctk.CTkTextbox(form_scroll_frame, height=120)
        self.textbox_bahan.pack(fill="x", padx=15, pady=(0, 10))
        
        # 3. Input Langkah Memasak
        ctk.CTkLabel(form_scroll_frame, text="Langkah Memasak (Satu langkah per baris):", anchor="w", font=ctk.CTkFont(size=16, weight="bold")).pack(fill="x", padx=15, pady=(10, 0))
        self.textbox_langkah = ctk.CTkTextbox(form_scroll_frame, height=200)
        self.textbox_langkah.pack(fill="x", padx=15, pady=(0, 20))
        
        # Tombol Simpan
        ctk.CTkButton(self, text="💾 Simpan Resep", command=self.simpan_resep_baru, 
                      font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20, padx=20, fill="x")

    def simpan_resep_baru(self):
        """Mengambil data dari form, menambahkannya, dan menyimpan ke JSON."""
        nama = self.entry_nama.get().strip()
        bahan = [b.strip() for b in self.textbox_bahan.get("1.0", "end-1c").split('\n') if b.strip()]
        langkah = [l.strip() for l in self.textbox_langkah.get("1.0", "end-1c").split('\n') if l.strip()]
        
        if not nama or not bahan or not langkah:
            ctk.CTkMessagebox.show_warning("Input Kurang", "Semua kolom Nama, Bahan, dan Langkah harus diisi.")
            return

        # Tentukan ID baru
        max_id = max((r['id'] for r in self.master.resep_data), default=0)
        new_id = max_id + 1
        
        resep_baru = {
            "id": new_id,
            "nama": nama,
            "bahan": bahan,
            "langkah": langkah
        }
        
        self.master.resep_data.append(resep_baru)
        simpan_resep(self.master.resep_data)
        
        ctk.CTkMessagebox.show_info("Berhasil", f"Resep '{nama}' berhasil ditambahkan!")
        self.master.show_frame("daftar")