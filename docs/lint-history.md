# 🧹 Dokumentasi: Script Pembersih Log Keylogger

## 📌 Ringkasan

Script ini digunakan untuk memproses file log **raw** yang dihasilkan oleh keylogger (`py-logger.py`) menjadi teks bersih yang lebih mudah dibaca.  
File hasil pembersihan akan disimpan di folder `output/cleaned/`.

---

## ⚙ Cara Kerja

### 1. **Penentuan Lokasi Folder**

- **Folder sumber (`source_dir`)** → `../output/raw` relatif terhadap lokasi script ini.
- **Folder output (`output_dir`)** → `../output/cleaned` relatif terhadap lokasi script ini.
- Jika folder output belum ada, script akan membuatnya secara otomatis:

  ```python
  os.makedirs(output_dir, exist_ok=True)
  ```

---

### 2. **Mapping Tombol Khusus**

- Tombol-tombol tertentu dari log diubah menjadi karakter yang dapat dibaca:

  | Tombol (`Key.<name>`) | Output Karakter |
  | --------------------- | --------------- |
  | `Key.space`           | (spasi)         |
  | `Key.enter`           | `\n` (enter)    |
  | `Key.tab`             | `\t` (tab)      |

- Anda dapat menambahkan mapping lain, misalnya:

  ```python
  "Key.down": "[DOWN_ARROW]"
  ```

---

### 3. **Penyaringan Log Tidak Relevan**

- Baris log yang diabaikan:

  - Baris dengan timestamp di awal.
  - Header seperti:

    ```txt
    === Starting key logger ===
    === Stopping key logger ===
    ```

  - Baris `"None"`.
- Regex yang digunakan:

  ```python
  re.compile(r"^\d{4}-\d{2}-\d{2}.*|=== Starting key logger ===|=== Stopping key logger ===")
  ```

---

### 4. **Penanganan Tombol**

- **`Key.backspace`** → Menghapus 1 karakter terakhir dari hasil sementara (`cleaned_text`).
- Tombol khusus lain (`Key.ctrl_l`, `Key.alt_l`, `Key.shift`, dll.) **dihilangkan**.
- Karakter biasa → hanya disimpan jika:

  - `isprintable()` **True**.
  - Bukan karakter kontrol ASCII (`0x00-0x1F` dan `0x7F`).

---

### 5. **Alur Pemrosesan**

1. Loop semua file `typing_history_*.txt` di folder `output/raw/`.
2. Baca file baris demi baris.
3. Bersihkan sesuai aturan di atas.
4. Simpan hasil bersih ke file:

   ```log
   cleaned_typing_history_YYYY-MM-DD_HH-MM-SS.txt
   ```

   di folder `output/cleaned/`.
5. Tampilkan status keberhasilan untuk setiap file.

---

## 📂 Struktur Folder Output

```log
output/
├── raw/
│   ├── typing_history_2025-08-09_10-17-53.txt
│   └── ...
└── cleaned/
    ├── cleaned_typing_history_2025-08-09_10-17-53.txt
    └── ...
```

---

## 🚀 Cara Menjalankan

### 1. **Menjalankan via Python**

- **Linux / Mac**

  ```bash
  python src/clean-history.py
  ```

- **Windows**

  ```powershell
  python src\clean-history.py
  ```

### 2. **Menjalankan via Makefile**

Jika sudah menambahkan target di `Makefile`:

```make
clean-output:
 @echo "Cleaning output logs..."
 python src/clean-history.py
```

Maka jalankan:

```powershell
make clean-output
```

---

## 📌 Catatan

- Pastikan folder `output/raw/` sudah berisi file log yang dihasilkan oleh script keylogger.
- Script ini **tidak menghapus file raw**, hanya membuat salinan bersih di `output/cleaned/`.
- Anda dapat memodifikasi `key_map` untuk menambahkan atau mengubah representasi tombol sesuai kebutuhan.
