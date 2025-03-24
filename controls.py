import pyautogui
import time

def attack_enemy(position):
    if position:
        pyautogui.moveTo(position[0], position[1])
        pyautogui.mouseDown()  # Simuler un clic gauche maintenu
        time.sleep(0.5)  # Maintenir l’attaque pendant 0.5 seconde
        pyautogui.mouseUp()  # Relâcher le clic
        time.sleep(0.1)  # Petite pause avant la prochaine action

def pickup_loot(position):
    if position:
        pyautogui.moveTo(position[0], position[1])
        pyautogui.click()
        time.sleep(0.1)
