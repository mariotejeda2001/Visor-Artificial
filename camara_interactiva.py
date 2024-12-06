import cv2
import numpy as np

# Inicializar la captura de video
cap = cv2.VideoCapture(0)

while True:
    # Capturar frame por frame
    ret, frame = cap.read()

    # Convertir a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Aplicar detección de bordes
    edges = cv2.Canny(gray, 100, 200)

    # Mostrar el frame original y el frame con detección de bordes
    cv2.imshow('Original', frame)
    cv2.imshow('Bordes', edges)

    # Salir del bucle si se presiona 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la captura y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()

