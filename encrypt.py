import os
import getpass
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.backends import default_backend

# --- Konfigurasi ---
SALT_SIZE = 16        # 128 bit
IV_SIZE = 16          # 128 bit
KEY_SIZE = 32         # 256 bit
ITERATIONS = 100_000
MAX_FILE_SIZE = 1 * 1024 * 1024  # 1 MB
MAGIC_HEADER = b"AES256ENC"      # Penanda file terenkripsi

backend = default_backend()


def generate_key_from_password(password, salt):
    """Mederivasi kunci AES-256 dari password menggunakan PBKDF2."""
    print("Mederivasi kunci dari password...")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=ITERATIONS,
        backend=backend
    )
    return kdf.derive(password.encode('utf-8'))


def encrypt_file(file_path, password):
    """Enkripsi file dengan AES-256 (CBC)."""
    if os.path.getsize(file_path) > MAX_FILE_SIZE:
        print(f"Error: Ukuran file melebihi batas {MAX_FILE_SIZE / (1024*1024)} MB.")
        return

    try:
        with open(file_path, 'rb') as f:
            plaintext = f.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' tidak ditemukan.")
        return

    salt = secrets.token_bytes(SALT_SIZE)
    iv = secrets.token_bytes(IV_SIZE)
    key = generate_key_from_password(password, salt)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    print("Melakukan enkripsi...")
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    output_file = file_path + ".enc"
    try:
        with open(output_file, 'wb') as f:
            f.write(MAGIC_HEADER)
            f.write(salt)
            f.write(iv)
            f.write(ciphertext)

        print(f"Sukses! File '{file_path}' telah dienkripsi ke '{output_file}'.")
    except IOError as e:
        print(f"Error saat menulis file: {e}")


def decrypt_file(file_path_encrypted, password):
    """Dekripsi file hasil enkripsi AES-256 (CBC)."""
    try:
        with open(file_path_encrypted, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path_encrypted}' tidak ditemukan.")
        return

    if not data.startswith(MAGIC_HEADER):
        print("Error: File ini bukan hasil enkripsi dari program ini.")
        return

    salt = data[len(MAGIC_HEADER):len(MAGIC_HEADER) + SALT_SIZE]
    iv = data[len(MAGIC_HEADER) + SALT_SIZE:len(MAGIC_HEADER) + SALT_SIZE + IV_SIZE]
    ciphertext = data[len(MAGIC_HEADER) + SALT_SIZE + IV_SIZE:]

    key = generate_key_from_password(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()

    try:
        print("Melakukan dekripsi...")
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    except Exception:
        print("Error: Dekripsi gagal. Kemungkinan password salah atau file korup.")
        return

    # Hilangkan ekstensi .enc agar nama kembali seperti semula
    output_file = file_path_encrypted.replace(".enc", "")
    try:
        with open(output_file, 'wb') as f:
            f.write(plaintext)
        print(f"Sukses! File '{file_path_encrypted}' telah didekripsi ke '{output_file}'.")
    except IOError as e:
        print(f"Error saat menulis file: {e}")


def main():
    """CLI sederhana untuk enkripsi dan dekripsi."""
    print("--- Aplikasi Kriptografi AES-256 (CBC) ---")

    while True:
        mode = input("Pilih mode: (1) Enkripsi, (2) Dekripsi, (q) Keluar: ").strip().lower()

        if mode == 'q':
            print("Keluar dari aplikasi.")
            break

        if mode not in ('1', '2'):
            print("Pilihan tidak valid.")
            continue

        file_path = input("Masukkan nama file (misal: 'data.csv'): ").strip()
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' tidak ditemukan.")
            continue

        try:
            password = getpass.getpass("Masukkan password rahasia: ")
            if not password:
                print("Password tidak boleh kosong.")
                continue
        except Exception as e:
            print(f"Error saat membaca password: {e}")
            continue

        if mode == '1':
            encrypt_file(file_path, password)
        else:
            if not file_path.endswith(".enc"):
                print("Info: Untuk dekripsi, gunakan file yang berekstensi .enc.")
            decrypt_file(file_path, password)

        print("-" * 40)


if __name__ == "__main__":
    main()
