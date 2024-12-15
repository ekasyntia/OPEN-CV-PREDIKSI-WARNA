import csv
import cv2
import numpy as np

# Konfigurasi Kamera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

# Nama file database
FileDB = 'DatabaseWarna.txt'

# Header untuk file CSV
header = ['B', 'G', 'R', 'Target']

# Buat file CSV jika belum ada
try:
    with open(FileDB, 'x', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
except FileExistsError:
    print(f"File {FileDB} sudah ada, melanjutkan penambahan data.")

print("Tekan tombol berikut untuk menambahkan data warna:")
print("1: Merah, 2: Hijau, 3: Biru, 4: Hitam, 5: Kuning, 6: Putih, ESC: Keluar")

while True:
    ret, img = cap.read()
    if not ret:
        print("Gagal membaca frame dari kamera.")
        break

    img = cv2.flip(img, 1)  # Membalikkan kamera jika terbalik

    # Ambil warna rata-rata dari area tertentu
    region = img[220:260, 330:340]  # Area yang dianalisis
    colorB = int(np.mean(region[:, :, 0]))
    colorG = int(np.mean(region[:, :, 1]))
    colorR = int(np.mean(region[:, :, 2]))
    color = [colorB, colorG, colorR]

    # Tampilkan area analisis dan warna rata-rata
    cv2.rectangle(img, (330, 220), (340, 260), (0, 255, 0), 2)
    cv2.putText(img, f"B: {colorB}, G: {colorG}, R: {colorR}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow("Database Color Capture", img)

    # Deteksi tombol untuk menentukan warna
    key = cv2.waitKey(30) & 0xFF
    if key == 27:  # ESC
        break
    elif key == ord('1'):
        label = "Merah"
    elif key == ord('2'):
        label = "Hijau"
    elif key == ord('3'):  # Biru
        label = "biru"
    elif key == ord('4'):  # Hitam
        label = "hitam"
    elif key == ord('5'):  # Kuning
        label = "kuning"
    elif key == ord('6'):  # Putih
        label = "putih"
    elif key == 27:  # ESC untuk keluar
        break
    else:
        continue

    # Simpan data ke file CSV
    with open(FileDB, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(color + [label])
        print(f"Data {color} dengan label '{label}' telah disimpan.")

cap.release()
cv2.destroyAllWindows()
