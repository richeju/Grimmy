import cv2
import numpy as np
import pyautogui

def find_enemy():
    screen_width, screen_height = pyautogui.size()
    detection_height = int(screen_height * 0.85)
    screenshot = pyautogui.screenshot(region=(0, 0, screen_width, detection_height))
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2HSV)
    
    lower_enemy = np.array([0, 30, 70])
    upper_enemy = np.array([30, 120, 180])
    mask = cv2.inRange(screenshot, lower_enemy, upper_enemy)
    
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    enemy_positions = []
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if 1000 < area < 10000:
            x, y, w, h = cv2.boundingRect(contour)
            if 30 < w < 200 and 50 < h < 300 and 0.5 < w/h < 1.5:
                enemy_x, enemy_y = x + w // 2, y + h // 2
                if 100 < enemy_x < screen_width - 100 and 200 < enemy_y < screen_height - 100:
                    enemy_positions.append((enemy_x, enemy_y))
    
    return enemy_positions if enemy_positions else None
