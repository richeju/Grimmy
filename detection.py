import cv2
import numpy as np
import pyautogui

def find_enemy():
    # Capture d’écran
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2HSV)
    
    # Définir la plage de couleur rouge (pour la barre de vie)
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    mask = cv2.inRange(screenshot, lower_red, upper_red)
    
    # Trouver les contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    enemy_positions = []
    
    for contour in contours:
        if cv2.contourArea(contour) > 100:  # Filtrer les petites zones
            x, y, w, h = cv2.boundingRect(contour)
            if 50 < w < 200 and 5 < h < 20:  # Taille typique d’une barre de vie
                enemy_positions.append((x + w // 2, y + h // 2))
    
    return enemy_positions if enemy_positions else None
