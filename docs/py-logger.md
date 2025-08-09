
# 📄 Dokumentasi: Python Simple Keylogger

## 🛠 Ringkasan

Script ini adalah keylogger sederhana berbasis Python yang menggunakan library [`pynput`](https://pypi.org/project/pynput/) untuk memantau input keyboard dan menyimpannya ke file log.  
Output log disimpan dalam format `.txt` di folder `output/raw/` dengan nama file yang mengandung timestamp.

---

## ⚙ Cara Kerja

### 1. **Penentuan Lokasi Output**

- Saat script dijalankan:
  - Jika **dijalankan sebagai file Python biasa** → `base_dir` diambil dari lokasi file `.py`
  - Jika **dijalankan sebagai binary hasil PyInstaller** → `base_dir` diambil dari lokasi executable `.exe`
- Folder output ditetapkan di:

```log
../output/raw
```

relatif terhadap `base_dir`.

---

### 2. **Pembuatan File Log**

- Nama file log otomatis mengikuti format:

```log
typing\_history\_YYYY-MM-DD\_HH-MM-SS.txt
```

Contoh:

```log
typing\_history\_2025-08-09\_10-17-53.txt
```

---

### 3. **Pencatatan Data**

- Fungsi `write_to_file(message, verbose=None)` digunakan untuk menulis ke file log.
- **Verbose Mode ON** → setiap entri disertai timestamp.
- **Verbose Mode OFF** → hanya mencatat karakter/tekanan tombol.
- Mapping penekanan tombol:
- Karakter biasa → disimpan langsung.
- Tombol spesial (`Key.space`, `Key.enter`, dll.) → disimpan dalam format `Key.<nama>`.

---

### 4. **Event Listener**

- **`on_press(key)`** → Mencatat setiap tombol yang ditekan.
- **`on_release(key)`** → Menghapus tombol dari set `pressed_keys` saat dilepas.
- Saat ini kode **tidak menghentikan logging dengan ESC**, karena barisnya dikomentari.
- **`on_press_track(key)`** → Menyimpan tombol ke `pressed_keys` lalu memanggil `on_press`.

---

### 5. **Alur Eksekusi**

1. Menentukan lokasi output dan membuat folder jika belum ada.
2. Membuat file log baru dengan nama timestamp.
3. Menulis header:

    ```txt
    \=== Starting key logger ===
    ```

4. Memulai `keyboard.Listener` untuk menangani penekanan dan pelepasan tombol.
5. Program berjalan hingga dihentikan secara manual (misalnya, `Ctrl+C` di terminal atau kill proses).

---

## 📂 Struktur Folder Output

```log
output/
└── raw/
├── typing\_history\_2025-08-09\_10-17-53.txt
├── typing\_history\_2025-08-09\_10-41-54.txt
└── ...
```

---

## 🚀 Cara Menjalankan

### 1. **Instalasi Dependensi**

Pastikan sudah membuat virtual environment dan menginstal `pynput`:

```bash
pip install pynput
```

### 2. **Menjalankan Script**

- **Linux / Mac**

  ```bash
  python src/py-logger.py
  ```

- **Windows**

  ```powershell
  python src\py-logger.py
  ```

---

## 🔧 Opsi Konfigurasi

| Variabel       | Tipe | Default | Deskripsi                                                              |
| -------------- | ---- | ------- | ---------------------------------------------------------------------- |
| `VERBOSE_MODE` | bool | False   | Jika `True`, setiap log disertai timestamp dan teks deskriptif tombol. |

---

## 📌 Catatan Penting

- Script ini **tidak otomatis berhenti** ketika ESC ditekan, karena kode penghentian di dalam `on_release()` dikomentari.
- Untuk mengaktifkan, buka komentar pada bagian:

  ```python
  if key == keyboard.Key.esc:
      write_to_file("=== Stopping key logger ===", verbose=True)
      print("Stopping key logger...")
      return False
  ```

- Gunakan **hanya untuk tujuan edukasi atau pengujian keamanan** dengan izin pihak terkait.
  Menggunakan keylogger tanpa izin adalah **ilegal**.
