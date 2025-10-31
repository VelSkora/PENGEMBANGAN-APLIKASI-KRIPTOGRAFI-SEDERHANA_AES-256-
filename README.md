# PENGEMBANGAN-APLIKASI-KRIPTOGRAFI-SEDERHANA_AES-256

==========================================
README - APLIKASI KRIPTOGRAFI AES-256 (CBC)
Mata Kuliah: Keamanan Data 
Nama: Avatar Bintang Ramadhan
NIM: 103052300007
Kelas: DS-47-01
==========================================

Aplikasi ini adalah implementasi sederhana dari algoritma AES-256 mode CBC
untuk mengenkripsi dan mendekripsi file, sebagai bagian dari tugas
individu .

Aplikasi ini menggunakan Python dan library 'cryptography' .

---
1. PRASYARAT (INSTALASI)
---

Pastikan kamu memiliki Python 3. Kamu perlu meng-install library `cryptography`.
Buka terminal (di VS Code atau CMD) dan jalankan:

pip install cryptography

---
2. CARA MENJALANKAN PROGRAM
---

Program ini dijalankan melalui Command Line (CLI) .

1. Buka terminal atau Command Prompt.
2. Arahkan ke folder tempat kamu menyimpan file `encrypt.py`.
3. Jalankan program dengan perintah:

   python encrypt.py

4. Program akan memandu kamu:
   - Pilih mode: (1) untuk Enkripsi, (2) untuk Dekripsi.
   - Masukkan nama file: Masukkan nama file yang ingin diproses (misal: `dataset.csv`) .
   - Masukkan password: Masukkan password rahasia (input akan tersembunyi).

---
3. CONTOH PENGGUNAAN
---

Misalkan kamu punya file `data_sensitif.csv` berukuran 500 KB.

A. ENKRIPSI
1. Jalankan `python encrypt.py`
2. Pilih mode: 1
3. Masukkan nama file: data_sensitif.csv
4. Masukkan password: (ketik password rahasiamu)
5. Program akan membuat file baru bernama `data_sensitif.csv.enc`.
   File ini berisi [SALT] + [IV] + [Ciphertext].

B. DEKRIPSI
1. Jalankan `python encrypt.py`
2. Pilih mode: 2
3. Masukkan nama file: data_sensitif.csv.enc (PENTING: masukkan nama file yang .enc)
4. Masukkan password: (ketik password yang SAMA seperti saat enkripsi)
5. Program akan membuat file baru bernama `data_sensitif.csv.decrypted`.
   Isi file ini akan sama persis dengan `data_sensitif.csv` asli.

---
4. CATATAN PENTING (FITUR & BATASAN)
---
- Key Derivation: Password tidak dipakai langsung. Program ini menggunakan PBKDF2 
  dengan SALT acak untuk membuat kunci 256-bit yang aman.
- IV: Setiap enkripsi menggunakan IV (Initialization Vector) acak baru
  untuk memastikan keamanan.
- Batasan: File input dibatasi maksimal 1 MB sesuai KAK .
- Error Handling: Program akan memberi peringatan jika file tidak ada 
  atau jika password dekripsi salah (unpadding gagal) .