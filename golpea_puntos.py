import cv2
import pygame
import numpy as np
import random
import mediapipe as mp

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Golpea los Puntos")

 # Inicializar la cámara
cap = cv2.VideoCapture(0)

# Configuración de MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

  # Configuración del juego
clock = pygame.time.Clock()
points = []
score = 0
font = pygame.font.Font(None, 36)

def create_point():
    x = random.randint(0, width)
    return {'pos': [x, 0], 'speed': random.randint(2, 5)}

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Capturar frame de la cámara
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar el frame")
        break
    
    # Detectar mano inicializacion de este 
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    # Convertir el frame a formato Pygame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    screen.blit(frame, (0,0))
    
    # Dibujar la mano y comprobar colisiones
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Obtener la posición de la punta del dedo índice
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x, y = int((1 - index_finger_tip.x) * width), int(index_finger_tip.y * height)
            
            # Dibujar un círculo en la punta del dedo índice
            pygame.draw.circle(screen, (0, 255, 255), (x, y), 10)
            
            # Comprobar colisiones con puntos
            for point in points[:]:
                if ((x - point['pos'][0])**2 + (y - point['pos'][1])**2)**0.5 < 20:
                    points.remove(point)
                    score += 1

    # Actualizar y dibujar puntos
    for point in points:
        point['pos'][1] += point['speed']
        pygame.draw.circle(screen, (255, 0, 0), [int(p) for p in point['pos']], 5)
        if point['pos'][1] > height:
            points.remove(point)

    # Añadir nuevos puntos
    if random.random() < 0.05:
        points.append(create_point())

    # Mostrar puntuación
    score_text = font.render(f"Puntuación: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Actualizar pantalla
    pygame.display.flip()
    clock.tick(30)

# Liberar recursos
cap.release()
hands.close()
pygame.quit()
