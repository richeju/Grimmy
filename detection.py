import cv2
import numpy as np
import pyautogui

def find_enemy():
    screen_width, screen_height = pyautogui.size()
    detection_height = int(screen_height * 0.85)
    screenshot = pyautogui.screenshot(region=(0, 0, screen_width, detection_height))
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2HSV)
    
    lower_enemy = np.array([0, 20, 50])
    upper_enemy = np.array([30, 100, 200])
    mask = cv2.inRange(screenshot, lower_enemy, upper_enemy)
    
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    enemy_positions = []
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if 500 < area < 20000:
            x, y, w, h = cv2.boundingRect(contour)
            if 20 < w < 300 and 20 < h < 400 and w/h < 2:
                enemy_positions.append((x + w // 2, y + h // 2))
    
    return enemy_positions if enemy_positions else None
