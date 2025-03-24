import pyautogui
import time

def attack_enemy(position):
    if position:
        pyautogui.moveTo(position[0], position[1])
        pyautogui.click()
        pyautogui.press('1')  # Utiliser une compétence
        time.sleep(0.5)

def pickup_loot():
    pyautogui.click(960, 540)  # Centre de l’écran, ajustable
    time.sleep(0.2)
