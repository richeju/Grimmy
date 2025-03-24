import pyautogui
import time

def attack_enemy(position):
    if position:
        pyautogui.moveTo(position[0], position[1])
        pyautogui.click()
        pyautogui.press('1')  # Utiliser une compétence
        time.sleep(0.3)  # Réduit pour plus de réactivité

def pickup_loot(position):
    if position:
        pyautogui.moveTo(position[0], position[1])  # Cliquer à la position de l’ennemi
        pyautogui.click()
        time.sleep(0.1)  # Réduit pour plus de réactivité
