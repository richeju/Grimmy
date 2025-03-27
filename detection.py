import cv2
import numpy as np
import pyautogui

def find_enemy():
    screen_width, screen_height = pyautogui.size()
    detection_height = int(screen_height * 0.85)
    screenshot = pyautogui.screenshot(region=(0, 0, screen_width, detection_height))
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2HSV)
    
    # Define red color ranges for the outline
    lower_red1 = np.array([0, 150, 150])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 150, 150])
    upper_red2 = np.array([180, 255, 255])
    
    # Create masks
    mask1 = cv2.inRange(screenshot, lower_red1, upper_red1)
    mask2 = cv2.inRange(screenshot, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    enemy_positions = []
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if 1000 < area < 10000:  # Adjust based on monster size
            x, y, w, h = cv2.boundingRect(contour)
            if 30 < w < 200 and 50 < h < 300 and 0.5 < w/h < 1.5:
                enemy_x, enemy_y = x + w // 2, y + h // 2
                if 100 < enemy_x < screen_width - 100 and 100 < enemy_y < detection_height - 100:
                    enemy_positions.append((enemy_x, enemy_y))
    
    return enemy_positions if enemy_positions else None
