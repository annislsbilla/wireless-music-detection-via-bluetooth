import socket
import sounddevice as sd
import numpy as np
import time

# Variabel global
n = [0, 0]

# Definisi perangkat input
input_devices = ['(hw:3,0)', '(hw:3,0)']  # Ganti dengan nama perangkat yang benar

# Parameter audio
FORMAT = 'int16'
CHANNELS = 1
RATE = 44100
CHUNK = 1024
THRESHOLD = 150

# Bendera deteksi audio
audio_detected = [0, 0]

# Buat socket Bluetooth
client_socks = [socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) for _ in range(2)]

# Hubungkan ke perangkat Orange Pi
addresses = [('E0:51:D8:21:63:27', 1), ('A0:67:20:F1:C2:9E', 1)]  # Ganti alamat sesuai perangkat
for i, sock in enumerate(client_socks):
    sock.connect(addresses[i])

# Konfigurasi stream audio
stream = sd.InputStream(
    device=input_devices,
    channels=CHANNELS,
    samplerate=RATE,
    dtype=FORMAT
)

with stream:
    print("Mendengarkan audio dari perangkat input... Tekan Ctrl+C untuk keluar.")
    try:
        while True:
            # Baca data audio
            indata_raw, overflowed = stream.read(CHUNK)

            # Analisis data audio
            indata = np.abs(indata_raw).mean()

            # Periksa level audio
            for i in range(2):
                if indata > THRESHOLD:
                    if n[i] <= 0:
                        n[i] = n[i] + 1
                        audio_detected[i] = 1
                        client_socks[i].send(b'1')
                else:
                    if n[i] > 0:
                        n[i] = 0
                        audio_detected[i] = 0
                        client_socks[i].send(b'0')

            # Proses data audio (opsional)

            # Cetak informasi
            print(f"Audio Detected: {audio_detected}, indata_raw: {indata}")

    except KeyboardInterrupt:
        print("Program dihentikan oleh pengguna.")
        for sock in client_socks:
            sock.close()


