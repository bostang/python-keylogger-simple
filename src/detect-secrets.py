import math
import re
from collections import Counter
from pathlib import Path
import os # Import os untuk Path

def calculate_shannon_entropy(s: str) -> float:
    """
    Menghitung Shannon Entropy dari sebuah string.
    Shannon Entropy mengukur tingkat ketidakpastian atau "randomness" dari data.
    Semakin tinggi entropi, semakin tidak terduga string tersebut.

    Args:
        s (str): String yang akan dihitung entropinya.

    Returns:
        float: Nilai Shannon Entropy dalam bit.
    """
    if not s:
        return 0.0

    # Menghitung frekuensi kemunculan setiap karakter
    char_counts = Counter(s)

    # Menghitung probabilitas setiap karakter
    total_chars = len(s)
    probabilities = [count / total_chars for count in char_counts.values()]

    # Menghitung Shannon Entropy menggunakan rumus: H = - sum(p_i * log2(p_i))
    # Kita hindari log(0) dengan memeriksa p > 0
    entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)

    return entropy

def check_char_set_diversity(s: str) -> int:
    """
    Memeriksa keragaman set karakter dalam string.
    Mengembalikan jumlah jenis karakter yang ditemukan (dari 4 kategori: lowercase, uppercase, digit, simbol).

    Args:
        s (str): String yang akan diperiksa keragaman karakternya.

    Returns:
        int: Jumlah kategori karakter yang ditemukan dalam string.
    """
    has_lower = bool(re.search(r'[a-z]', s))
    has_upper = bool(re.search(r'[A-Z]', s))
    has_digit = bool(re.search(r'[0-9]', s))
    # Simbol adalah karakter apa pun yang bukan huruf (baik besar/kecil), angka, atau spasi
    has_symbol = bool(re.search(r'[^a-zA-Z0-9\s]', s))

    diversity_count = sum([has_lower, has_upper, has_digit, has_symbol])
    return diversity_count

def detect_potential_secrets(directory_path: str, # Diubah dari file_path menjadi directory_path
                             entropy_threshold_per_char: float = 2.0, 
                             min_length: int = 8, 
                             min_diversity_types: int = 3) -> list[dict]:
    """
    Mendeteksi string yang berpotensi menjadi secrets/password dalam SEMUA file teks
    di dalam direktori yang ditentukan, menggunakan kombinasi Shannon Entropy dan keragaman set karakter.

    Args:
        directory_path (str): Path menuju direktori yang akan dianalisis.
        entropy_threshold_per_char (float): Ambang batas entropi per karakter.
                                            String yang entropi per karakternya di atas nilai ini akan ditandai.
        min_length (int): Panjang minimum string yang akan dipertimbangkan.
        min_diversity_types (int): Jumlah minimum jenis karakter (lowercase, uppercase, digit, symbol)
                                   yang harus dimiliki string agar dianggap berpotensi secret.

    Returns:
        list[dict]: Daftar dictionary, di mana setiap dictionary berisi detail string yang terdeteksi,
                    termasuk nama file asal.
    """
    all_potential_secrets = []

    # Pastikan directory_path adalah Path object
    dir_path = Path(directory_path)

    # Periksa apakah direktori ada
    if not dir_path.is_dir():
        print(f"Error: Direktori '{directory_path}' tidak ditemukan.")
        return []

    # Iterasi melalui setiap file .txt di direktori yang ditentukan
    for file_path in dir_path.glob("*.txt"): # Mencari semua file .txt
        print(f"Menganalisis file: {file_path.name}")
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Error saat membaca file '{file_path.name}': {e}")
            continue # Lanjut ke file berikutnya jika ada error

        # Memisahkan teks menjadi "token" (kata-kata atau urutan karakter) berdasarkan spasi atau tab.
        tokens = re.split(r'\s+', content)

        for token in tokens:
            # Hapus spasi di awal/akhir token jika ada
            token = token.strip()
            
            # Abaikan token kosong setelah stripping
            if not token:
                continue

            # Periksa panjang minimum token
            if len(token) >= min_length:
                total_entropy = calculate_shannon_entropy(token)
                
                # Hitung entropi per karakter. Ini lebih baik untuk perbandingan string dengan panjang berbeda.
                entropy_per_char = total_entropy / len(token) if len(token) > 0 else 0.0
                
                # Periksa keragaman set karakter
                diversity_count = check_char_set_diversity(token)

                # Kriteria deteksi:
                # 1. Entropi per karakter di atas ambang batas (untuk string yang sangat acak) ATAU
                # 2. Keragaman set karakter di atas ambang batas (untuk password umum yang kompleks)
                if (entropy_per_char >= entropy_threshold_per_char) or \
                   (diversity_count >= min_diversity_types):
                    
                    all_potential_secrets.append({
                        "string": token,
                        "file": file_path.name, # Tambahkan nama file asal
                        "total_entropy_bits": total_entropy,
                        "entropy_per_char": entropy_per_char,
                        "char_diversity_types": diversity_count
                    })
                    
    return all_potential_secrets

# --- Contoh Penggunaan ---
# Menggunakan struktur proyek yang Anda berikan
base_dir = Path(__file__).resolve().parent # src/
cleaned_output_dir = base_dir.parent / "output" / "cleaned" # output/cleaned/

# Untuk tujuan demonstrasi, kita akan membuat direktori dummy dan file dummy
# jika belum ada, berdasarkan contoh yang Anda berikan.
dummy_cleaned_dir = cleaned_output_dir # Gunakan path yang sebenarnya untuk dummy

os.makedirs(dummy_cleaned_dir, exist_ok=True) # Pastikan direktori dummy ada



print(f"Menganalisis direktori: {cleaned_output_dir}\n")

# Panggil fungsi deteksi untuk seluruh direktori
# Parameter default: entropy_threshold_per_char=2.0, min_length=8, min_diversity_types=3
detected_secrets = detect_potential_secrets(str(cleaned_output_dir))

if detected_secrets:
    print("Potensi secrets/password yang ditemukan:")
    for secret in detected_secrets:
        print(f"- '{secret['string']}' (File: {secret['file']}, Entropi total: {secret['total_entropy_bits']:.2f} bit, Entropi per karakter: {secret['entropy_per_char']:.2f} bit/char, Keragaman karakter: {secret['char_diversity_types']} jenis)")
else:
    print("Tidak ada potensi secrets/password dengan kriteria tinggi yang terdeteksi di direktori.")

