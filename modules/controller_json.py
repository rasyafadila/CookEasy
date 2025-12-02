# modules/json_handler.py

import json
import os

DATA_FILE = 'data/resep.json'

def muat_resep():
    """Memuat data resep dari file JSON. Mengembalikan list kosong jika gagal."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # Menangani jika file JSON kosong, rusak, atau tidak ditemukan.
        return []

def simpan_resep(resep_list):
    """Menyimpan data resep ke file JSON."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(resep_list, f, indent=2)