# import library

import time ## mengimport library time
import sqlite3

# koneksi ke database sqlite
conn = sqlite3.connect('cashier.db')
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transaction'")
result = cur.fetchone()

if result is None:
    cur.execute('''CREATE TABLE "transaction"
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama_item TEXT NOT NULL,
                    jumlah_item INTEGER NOT NULL,
                    harga REAL NOT NULL,
                    total_harga REAL NOT NULL,
                    diskon REAL,
                    harga_diskon REAL)''')
    conn.commit()

# membuat class Transaction
class Transaction:
    
    def __init__(self): ## fungsi untuk inisialisasi objek
        self.items = [] ## inisialisasi items dengan list kosong
        
    def add_item(self, item): ## fungsi untuk menambahkan item ke dalam list items
        self.items.append(item)
        
    def update_item_name(self, old_name, new_name): ## fungsi untuk mengubah nama item
        for item in self.items:
            if item[0] == old_name: ## jika nama item sama dengan old_name
                item[0] = new_name ## maka ganti nama item dengan new_name
                
    def update_item_qty(self, name, new_qty): ## fungsi untuk mengubah jumlah item
        for item in self.items:
            if item[0] == name: ## jika nama item sama dengan name
                item[1] = new_qty ## maka ganti jumlah item dengan new_qty
                
    def update_item_price(self, name, new_price): ## fungsi untuk mengubah harga item
        for item in self.items:
            if item[0] == name: ## jika nama item sama dengan name
                item[2] = new_price ## maka ganti harga item dengan new_price
                
    def delete_item(self, name): ## fungsi untuk menghapus item
        for item in self.items:
            if item[0] == name: ## jika nama item sama dengan name
                self.items.remove(item) ## maka hapus item dari list items
                
    def reset_transaction(self): ## fungsi untuk mereset transaksi
        self.items = [] ## mengosongkan list items
        
    def check_order(self): ## fungsi untuk memeriksa pesanan
        for item in self.items:
            if len(item) != 3: ## jika panjang item tidak sama dengan 3
                return "Terdapat kesalahan input data" ## maka return string pesan error
        return "Pemesanan sudah benar" ## jika tidak ada error, maka return string pesan sukses
        
    def check_out(self): ## fungsi untuk check out
        total_harga = 0 ## inisialisasi total harga dengan 0
        for item in self.items:
            total_harga += item[1] * item[2] ## menghitung total harga
        
        diskon = 0 ## inisialisasi diskon dengan 0
        if total_harga > 500000: ## jika total harga lebih besar dari 500000
            diskon = 0.07 ## maka diskon sebesar 7%
        elif total_harga > 300000: ## jika total harga lebih besar dari 300000
            diskon = 0.06 ## maka diskon sebesar 6%
        elif total_harga > 200000: ## jika total harga lebih besar dari 200000
            diskon = 0.05 ## maka diskon sebesar 5%
            
        harga_diskon = total_harga - total_harga * diskon ## menghasilkan harga akhir / total harga yang dibayarkan customer
        
        return harga_diskon
    
    # Method untuk mencetak transaksi
    def print_transaction(self):
        print("| No | Nama Item | Jumlah Item | Harga/Item | Total Harga |")
        print("|----|-----------|-------------|------------|-------------|")
        # Looping untuk mencetak setiap item yang ditambahkan
        for i, item in enumerate(self.items):
             # Mendapatkan nama, jumlah, harga, dan total harga item
            nama_item = item[0]
            jumlah_item = item[1]
            harga = item[2]
            total_harga = jumlah_item * harga
            # Mencetak baris tabel untuk item tersebut
            print(f"| {i+1}  | {nama_item}     | {jumlah_item}           | {harga}       | {total_harga}        |")


    def insert_to_table(self):
        cur = conn.cursor()
        # Looping untuk setiap item yang ditambahkan
        for i, item in enumerate(self.items):
             # Mendapatkan nama, jumlah, harga, dan total harga item
            nama_item = item[0]
            jumlah_item = item[1]
            harga = item[2]
            total_harga = jumlah_item * harga

             # Inisialisasi diskon dan harga setelah diskon
            diskon = 0
            harga_diskon = total_harga

            # Mendapatkan nilai diskon berdasarkan total harga
            if total_harga > 500000:
                diskon = 0.07
            elif total_harga > 300000:
                diskon = 0.06
            elif total_harga > 200000:
                diskon = 0.05
            
             # Menghitung harga setelah diskon
            harga_diskon = total_harga - total_harga * diskon
             # Menambahkan item ke tabel transaksi di database
            cur.execute(
                 'INSERT INTO "transaction" (nama_item, jumlah_item, harga, total_harga, diskon, harga_diskon) VALUES (?, ?, ?, ?, ?, ?)',
                 (nama_item, jumlah_item, harga, total_harga, diskon, harga_diskon))
        # Commit transaksi dan menutup koneksi ke database    
        conn.commit()
        cur.close()
        conn.close()

def input_transaction():
    transaction = Transaction()
    # Looping untuk menjalankan program dan memasukan input item
    while True:
        nama_item = input("Nama item: ")

        while True:
            try:
                jumlah_item = int(input("Jumlah item: "))
                break
            except ValueError:
                print("Input tidak valid. Harap masukkan angka.")
        
        while True:
            try:
                harga = float(input("Harga/item: "))
                break
            except ValueError:
                print("Input tidak valid. Harap masukkan angka.")

        # Menambahkan item ke transaksi
        transaction.add_item([nama_item, jumlah_item, harga])

        # Meminta input untuk menambah item lagi atau tidak
        tambah_lagi = input("Tambah item lagi? (y/n): ")
        while tambah_lagi.lower() not in ['y', 'n']:
            print("Input tidak valid, silakan masukkan y atau n")
            print("")
            tambah_lagi = input("Tambah item lagi? (y/n): ")
        if tambah_lagi.lower() == 'n':
            break
    
    # Mencetak transaksi saat ini
    transaction.print_transaction()
    print("")

    # Looping untuk memodifikasi atau menghapus item
    while True:
         # Meminta input untuk mengubah/hapus item atau tidak
        print("Apakah ada item yang ingin diubah/hapus? (y/n): ")
        print("")
        ubah_hapus = input()
        while ubah_hapus.lower() not in ['y', 'n']:
            print("Input tidak valid, silakan masukkan y atau n")
            print("")
            ubah_hapus = input("Apakah ada item yang ingin diubah/hapus? (y/n):")

        # Jika tidak ingin mengubah/hapus, keluar dari loop
        if ubah_hapus.lower() == 'n':
            break
        
         # Meminta input dari user mengenai nomor item yang ingin diubah atau dihapus
        no_item = int(input("Masukan Nomor item yang ingin diubah/hapus: "))
        print("")
        while no_item < 1 or no_item > len(transaction.items):
            print("Input tidak valid. Harap masukkan nomor item yang valid.")
            print("")
            no_item = int(input("Masukkan nomor item yang ingin diubah/hapus: "))
        print(f"{nama_item} anda pilih untuk dihapus atau diganti")
        print("")

        # Meminta input dari user mengenai opsi apa yang ingin dilakukan pada item tersebut
        pilihan = int(input("Masukkan pilihan: 1. Ubah nama item, 2. Ubah jumlah item, 3. Ubah harga item, 4. Hapus item"))
        print("")
        while pilihan not in [1, 2, 3, 4]:
            print("Input tidak valid. Harap masukkan angka antara 1 sampai 4.")
            print("")
            pilihan = int(input("Masukkan pilihan: 1. Ubah nama item, 2. Ubah jumlah item, 3. Ubah harga item, 4. Hapus item: "))

        if pilihan == 1:
            # Meminta input dari user mengenai nama item baru
            new_nama_item = input("Masukkan nama item baru: ")
             # Mengubah nama item pada objek Transaction
            transaction.update_item_name(transaction.items[no_item-1][0], new_nama_item)
        elif pilihan == 2:
             # Meminta input dari user mengenai jumlah item baru
            new_jumlah_item = int(input("Masukkan jumlah item baru: "))
             # Mengubah jumlah item pada objek Transaction
            transaction.update_item_qty(transaction.items[no_item-1][0], new_jumlah_item)
        elif pilihan == 3:
            # Meminta input dari user mengenai harga item baru
            new_harga_item = float(input("Masukkan harga item baru: "))
            # Mengubah harga item pada objek Transaction
            transaction.update_item_price(transaction.items[no_item-1][0], new_harga_item)
        elif pilihan == 4:
             # Menghapus item dari objek Transaction
            transaction.delete_item(transaction.items[no_item-1][0])
            print("Item berhasil dihapus")
        else:
            print("Pilihan tidak valid")

         # Mencetak transaksi setelah dilakukan perubahan atau penghapusan item
        transaction.print_transaction()
        print("")

    print("Hasil transaksi:")
    # Mencetak transaksi
    transaction.print_transaction()
    print("")

    while True:
        benar = input("Apakah transaksi sudah benar? (y/n): ")
        print("")
        while benar.lower() not in ['y', 'n']:
            print("Input tidak valid. Harap masukkan 'y' atau 'n'.")
            print("")
            benar = input("Apakah transaksi sudah benar? (y/n): ")
        if benar.lower() == 'y':
            break
        
        reset = input("Apakah ingin mereset transaksi? (y/n): ")
        print("")
        while reset.lower() not in ['y', 'n']:
            print("Input tidak valid. Harap masukkan 'y' atau 'n'.")
            print("")
            reset = input("Apakah ingin mereset transaksi? (y/n): ")
        if reset.lower() == 'y':
             # Mereset transaksi
            transaction.reset_transaction()
            # Mencetak transaksi setelah direset
            transaction.print_transaction()
            print("Semua Item berhasil didelete!")
            # Memanggil kembali fungsi input_transaction
            return input_transaction()

        transaction.print_transaction()
        print("")

    order_check = transaction.check_order()
    if order_check != "Pemesanan sudah benar":
        print(order_check)
    else:
        # Check out dan masukkan ke database
        harga_setelah_diskon = transaction.check_out()
        conn.cursor()
        transaction.insert_to_table()
        print("Total harga setelah diskon: ", harga_setelah_diskon)
    
input_transaction()