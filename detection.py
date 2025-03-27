import cv2
import numpy as np
import pyautogui
import time

def find_potential_enemies():
    screen_width, screen_height = pyautogui.size()
    detection_height = int(screen_height * 0.85)
    screenshot = pyautogui.screenshot(region=(0, 0, screen_width, detection_height))
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2HSV)
    
    # Définir une plage de couleur pour les ennemis potentiels (teintes de peau ou armures)
    lower_enemy = np.array([0, 30, 70])
    upper_enemy = np.array([30, 120, 180])
    mask = cv2.inRange(screenshot, lower_enemy, upper_enemy)
    
    # Appliquer un flou pour réduire le bruit
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    
    # Trouver les contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    potential_positions = []
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if 1000 < area < 10000:
            x, y, w, h = cv2.boundingRect(contour)
            if 30 < w < 200 and 50 < h < 300 and 0.5 < w/h < 1.5:
                enemy_x, enemy_y = x + w // 2, y + h // 2
                if 100 < enemy_x < screen_width - 100 and 200 < enemy_y < screen_height - 100:
                    potential_positions.append((enemy_x, enemy_y))
    
    return potential_positions if potential_positions else None

def confirm_enemy(position):
    # Déplacer la souris sur la position pour cibler le monstre
    pyautogui.moveTo(position[0], position[1])
    time.sleep(0.1)  # Attendre que le contour rouge apparaisse
    
    # Prendre une petite capture autour de la position
    x, y = position
    region_size = 50  # Taille de la région autour de la position
    screenshot = pyautogui.screenshot(region=(x - region_size, y - region_size, region_size * 2, region_size * 2))
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2HSV)
    
    # Définir les plages de rouge pour le contour
    lower_red1 = np.array([0, 150, 150])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 150, 150])
    upper_red2 = np.array([180, 255, 255])
    
    # Créer les masques
    mask1 = cv2.inRange(screenshot, lower_red1, upper_red1)
    mask2 = cv2.inRange(screenshot, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)
    
    # Vérifier si un contour rouge est présent
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if 50 < area < 500:  # Taille typique d'un contour rouge
            return True
    return False

def find_enemy():
    potential_positions = find_potential_enemies()
    if not potential_positions:
        return None
    
    confirmed_positions = []
    for pos in potential_positions:
        if confirm_enemy(pos):
            confirmed_positions.append(pos)
    
    return confirmed_positions if confirmed_positions else None
