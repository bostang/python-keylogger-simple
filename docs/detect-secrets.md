# 📄 Dokumentasi — Deteksi Potensi Secrets/Password di File Teks

## 1. Deskripsi Singkat

Script ini digunakan untuk **mendeteksi string yang berpotensi menjadi password atau secrets** dari sekumpulan file teks dalam sebuah direktori.
Pendekatan deteksi memanfaatkan:

* **Shannon Entropy** — mengukur tingkat keacakan suatu string.
* **Keragaman set karakter** — menghitung berapa jenis karakter berbeda yang digunakan (huruf kecil, huruf besar, angka, simbol).

String dengan entropi tinggi atau keragaman karakter yang kompleks cenderung merupakan password atau secrets.

---

## 2. Fitur Utama

* Menghitung **Shannon Entropy** untuk setiap token (kata atau rangkaian karakter).
* Menghitung **keragaman set karakter** dari 4 kategori:

  1. Huruf kecil (`a-z`)
  2. Huruf besar (`A-Z`)
  3. Angka (`0-9`)
  4. Simbol (karakter selain huruf, angka, atau spasi)
* Mendukung **analisis massal** untuk semua file `.txt` di direktori.
* Mengabaikan token yang terlalu pendek atau tidak memenuhi kriteria keragaman.
* Output berupa daftar string mencurigakan dengan metadata:

  * Nama file asal
  * Entropi total
  * Entropi per karakter
  * Jumlah jenis karakter

---

## 3. Struktur Direktori yang Dianjurkan

```log
project/
│
├─ src/
│   ├─ detect_secrets.py     # Script pendeteksi ini
│
├─ output/
│   ├─ cleaned/              # Berisi file teks hasil pembersihan dari keylogger
│       ├─ cleaned_file1.txt
│       ├─ cleaned_file2.txt
│       └─ ...
```

---

## 4. Parameter Utama Fungsi

### `detect_potential_secrets(directory_path, entropy_threshold_per_char=2.0, min_length=8, min_diversity_types=3)`

| Parameter                    | Tipe    | Default | Deskripsi                                                                        |
| ---------------------------- | ------- | ------- | -------------------------------------------------------------------------------- |
| `directory_path`             | `str`   | -       | Path direktori berisi file teks yang akan dianalisis.                            |
| `entropy_threshold_per_char` | `float` | `2.0`   | Ambang batas entropi per karakter untuk menandai string sebagai potensi secrets. |
| `min_length`                 | `int`   | `8`     | Panjang minimum token agar dipertimbangkan sebagai kandidat secrets.             |
| `min_diversity_types`        | `int`   | `3`     | Jumlah minimal jenis karakter berbeda (dari 4 kategori) agar dianggap kompleks.  |

---

## 5. Alur Kerja Script

1. **Menentukan direktori target** (`output/cleaned/`).
2. **Membaca setiap file `.txt`** di direktori tersebut.
3. **Memecah konten file** menjadi token berdasarkan spasi/tab.
4. **Memfilter token**:

   * Panjang minimal `min_length`
   * Memenuhi minimal entropi atau keragaman karakter
5. **Menghitung metrik**:

   * Entropi total (`bit`)
   * Entropi per karakter (`bit/char`)
   * Jumlah kategori karakter
6. **Menyimpan hasil** ke dalam list dictionary.
7. **Menampilkan hasil** di terminal.

---

## 6. Contoh Penggunaan

```bash
# Jalankan script dari folder src
python detect_secrets.py
```

Output contoh:

```log
Menganalisis direktori: /path/to/project/output/cleaned

Menganalisis file: cleaned_typing_history_2025-08-09_12-30-15.txt
Potensi secrets/password yang ditemukan:
- 'P@ssw0rd123!' (File: cleaned_typing_history_2025-08-09_12-30-15.txt, Entropi total: 39.31 bit, Entropi per karakter: 3.28 bit/char, Keragaman karakter: 4 jenis)
```

---

## 7. Penyesuaian dan Tips

* **Ingin lebih ketat?**
  Naikkan `entropy_threshold_per_char` atau `min_length`.
* **Ingin lebih longgar?**
  Turunkan `entropy_threshold_per_char` atau `min_diversity_types`.
* **Menganalisis folder lain:**
  Ubah variabel:

  ```python
  cleaned_output_dir = Path("/path/ke/folder/lain")
  ```

---

## 8. Keterbatasan

* Tidak mendeteksi secrets yang sangat pendek meski berkarakter unik.
* Tidak membedakan antara *random string* yang asli dengan data terenkripsi atau hash.
* Hanya membaca file teks (`.txt`), tidak memproses format biner.
