# Panduan Upload File ke GitHub Private Repo dengan Fine-grained PAT

## **1. Tujuan Script**

Script ini digunakan untuk:

* Mengambil semua file `.txt` dari folder `output/cleaned`
* Mengunggahnya ke **private repository GitHub**
* Jika file sudah ada → **update**
* Jika belum ada → **create**

---

## **2. Prasyarat**

* Python 3.8+
* Paket **PyGithub** dan **python-dotenv**
* **Private repository GitHub** sudah dibuat
* Fine-grained Personal Access Token (FG-PAT) dengan permission minimal

---

## **3. Instalasi Library**

Jalankan di terminal:

```bash
pip install PyGithub python-dotenv
```

---

## **4. Membuat Fine-grained Personal Access Token**

1. Masuk ke [Settings → Developer settings → Personal access tokens → Fine-grained tokens](https://github.com/settings/tokens?type=beta)
2. Klik **Generate new token**
3. **Repository access**:

   * Pilih **Only select repositories**
   * Pilih repo tujuan
4. **Repository permissions**:

   * **Contents** → `Read and write` ✅
   * **Metadata** → `Read-only` ✅
5. **Account permissions**:

   * Semua → `No access`
6. Klik **Generate token**, simpan token yang muncul (hanya tampil sekali).

---

## **5. Membuat File `.env`**

Letakkan `.env` di **root project** (sejajar dengan folder `src` dan `output`).

Contoh isi `.env`:

```env
GITHUB_TOKEN=ghp_xxx_yang_kamu_dapatkan_dari_FG-PAT
GITHUB_REPO=username/nama-repo
GITHUB_BRANCH=main
```

> **Catatan**: Jangan commit file `.env` ke repo. Tambahkan `.env` ke `.gitignore`.

---

## **6. Struktur Folder Project**

```
python_keylogger_simple/
│
├── .env
├── src/
│   └── upload-to-github.py
├── output/
│   └── cleaned/
│       ├── file1.txt
│       ├── file2.txt
│       └── ...
└── venv/
```

---

## **7. Menjalankan Script**

Dari root project:

```bash
python src/upload-to-github.py
```

---

## **8. Troubleshooting**

### **403: Resource not accessible by personal access token**

* Pastikan FG-PAT memiliki **Contents → Read and write**
* Pastikan repo sudah dipilih di **Only select repositories**
* Pastikan kamu push ke branch yang ada (`main` atau `master`)

### **404: Repository is empty**

* Buat commit awal di repo (README.md atau file kosong) sebelum menjalankan script.

---

## **9. Keamanan**

* **Jangan simpan token langsung di kode**
* Gunakan `.env` untuk menyimpan credential
* Tambahkan `.env` ke `.gitignore`
* Gunakan FG-PAT dengan scope minima