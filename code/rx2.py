import socket

# Alamat Orange Pi 2
address = ("A0:67:20:F1:C2:9E", 1)

# Buat socket Bluetooth
server_sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

# Bind ke alamat
server_sock.bind(address)
server_sock.listen(1)

print("Menunggu koneksi...")
client_sock, _ = server_sock.accept()
print("Koneksi diterima dari Raspberry Pi 1")

try:
    while True:
        data = client_sock.recv(1024).decode()
        if not data:
            break  # Hentikan loop jika tidak ada data yang diterima (koneksi ditutup)

        if data == "1":
            print("Orange Pi 2: Ada musik")
        else:
            print("Orange Pi 2: Tidak ada musik")

except Exception as e:
    print(f"Terjadi kesalahan di Orange Pi 2: {e}")

finally:
    print("Menutup koneksi Orange Pi 2...")
    client_sock.close()
    server_sock.close()
    print("Koneksi Orange Pi 2 ditutup.")

