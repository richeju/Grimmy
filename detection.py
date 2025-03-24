import cv2
import numpy as np
import pyautogui

def find_enemy():
    # Capture d’écran
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    
    # Charger l’image de la barre de vie ennemie
    enemy_template = cv2.imread('assets/enemy_healthbar.png')
    
    # Recherche du template
    result = cv2.matchTemplate(screenshot, enemy_template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    locations = np.where(result >= threshold)
    
    if len(locations[0]) > 0:
        y, x = locations[0][0], locations[1][0]
        return (x + enemy_template.shape[1] // 2, y + enemy_template.shape[0] // 2)
    return None
