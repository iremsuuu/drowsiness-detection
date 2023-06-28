
import cv2
import numpy as np
import time
import winsound

# Alarm sesi
def play_alarm_sound():
    winsound.PlaySound("alarm_sound.wav", winsound.SND_ASYNC)

# Video Akışı
video_capture = cv2.VideoCapture(0)

# Göz Degiskenleri
GOZ_KAPALI = False
SAYAC = 0
ALARM_ACIK = False
UYANDIRMA_EKRANI = False
UYANDIRMA_EKRANI_SURESI = 2 
YESIL = (0, 255, 0)  
KIRMIZI = (0, 0, 255) 

# Yazı
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_thickness = 2

# Sayaç
sayac_suresi = 5

while True:
    # Görüntü Alımı
    ret, frame = video_capture.read()

    # Renk Dönüşümü
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Göz Tespiti
    eyes = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
    eye_rects = eyes.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30))

    # Göz Kontrolü
    eyes_found = len(eye_rects) > 0

    if eyes_found:
        SAYAC = 0
    else:
        SAYAC += 1

    # Sayaç Başlatma
    if SAYAC == 1:
        baslagic_zamani = time.time()

    # Sayaç Kontrolü
    if SAYAC >= 1 and time.time() - baslagic_zamani >= sayac_suresi:
        if not ALARM_ACIK:
            ALARM_ACIK= True
            play_alarm_sound()
            uyanma_saati_baslat = time.time()

    # Alarm Aktiflik
    if ALARM_ACIK:
        cv2.putText(frame, "Alarm!", (50, 100), font, font_scale, KIRMIZI, font_thickness)
        if eyes_found:
            UYANDIRMA_EKRANI = True
            if time.time() - uyanma_saati_baslat <= UYANDIRMA_EKRANI_SURESI:
                cv2.putText(frame, "Uyandiniz!", (50, 50), font, font_scale, YESIL, font_thickness)
                cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), YESIL, 10)
            else:
             ALARM_ACIK = False
    # Göz Çerçevesi
    elif eyes_found:
        for (x, y, w, h) in eye_rects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), YESIL, 2)
        if UYANDIRMA_EKRANI:
            cv2.putText(frame, "Uyandiniz!", (50, 50), font, font_scale, YESIL, font_thickness)
            cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), YESIL, 10)
            if time.time() - uyanma_saati_baslat>= UYANDIRMA_EKRANI_SURESI * 2:
                UYANDIRMA_EKRANI = False

    # Sayaç Gösterimi
    else:
        cv2.putText(frame, f"Uyku Modu: {sayac_suresi- int(time.time() - baslagic_zamani)}", (50, 50), font, font_scale, KIRMIZI, font_thickness)

    # Ekranı gösterme
    cv2.imshow("Uyku Hali Uyari Dedektoru!", frame)

    # 'q' tuşuna basıldığında döngüden çıkma
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Sistemi Kapatma
video_capture.release()
cv2.destroyAllWindows()