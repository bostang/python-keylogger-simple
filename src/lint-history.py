import os
import re
from pathlib import Path

# Tentukan lokasi folder output relatif terhadap file ini
base_dir = os.path.dirname(os.path.abspath(__file__))
source_dir = os.path.abspath(os.path.join(base_dir, "..", "output/raw"))
output_dir = os.path.abspath(os.path.join(base_dir, "..", "output/cleaned"))
os.makedirs(output_dir, exist_ok=True)

# Mapping key ke karakter yang diinginkan
key_map = {
    "Key.space": " ",
    "Key.enter": "\n",
    "Key.tab": "\t",
    # Anda bisa menambahkan mapping lain jika diperlukan,
    # misalnya "Key.down" : "[DOWN_ARROW]" jika ingin mencatatnya.
}

# Kompilasi regex untuk mendeteksi baris log yang tidak relevan (timestamp atau header)
# Menggunakan '^' untuk memastikan pola cocok dari awal baris.
log_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}.*|=== Starting key logger ===|=== Stopping key logger ===")

# Proses semua file typing_history yang ada di folder sumber
for file_path in sorted(Path(source_dir).glob("typing_history_*.txt")):
    cleaned_text = ""
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            # Hapus spasi di awal/akhir baris
            line = line.strip()

            # 1. Skip baris yang merupakan timestamp atau header log
            if log_pattern.match(line):
                continue

            # 2. Abaikan baris yang secara eksplisit adalah "None"
            # Ini menangani kasus seperti baris tunggal "None" yang muncul di log.
            if line == "None":
                continue

            # 3. Tangani special keys yang perlu dikonversi ke karakter yang dapat dibaca
            if line in key_map:
                cleaned_text += key_map[line]
            # 4. Tangani Key.backspace dengan menghapus karakter terakhir
            elif line == "Key.backspace":
                cleaned_text = cleaned_text[:-1]
            # 5. Abaikan special keys lain yang diawali "Key."
            # Contoh: Key.ctrl_l, Key.alt_l, Key.shift, dll., tidak akan ditambahkan.
            elif line.startswith("Key."):
                continue
            # 6. Untuk baris yang tersisa (seharusnya karakter biasa), filter karakter non-printable
            else:
                cleaned_chars = []
                for char in line:
                    # Pastikan karakter dapat dicetak DAN bukan merupakan karakter kontrol ASCII
                    # Karakter kontrol ASCII berkisar dari 0x00-0x1F dan 0x7F (DEL).
                    # 'isprintable()' akan mengembalikan False untuk sebagian besar dari mereka,
                    # tetapi ini menambahkan lapisan keamanan ekstra.
                    if char.isprintable() and not (0x00 <= ord(char) <= 0x1F) and not (ord(char) == 0x7F):
                        cleaned_chars.append(char)
                cleaned_text += "".join(cleaned_chars)

    # Simpan teks yang sudah dibersihkan ke file baru di folder output
    cleaned_file = Path(output_dir) / f"cleaned_{file_path.name}"
    with open(cleaned_file, "w", encoding="utf-8") as f:
        f.write(cleaned_text)

    print(f"[OK] File '{file_path.name}' berhasil dibersihkan menjadi '{cleaned_file.name}'.")

print("Proses pembersihan semua file riwayat pengetikan telah selesai.")
