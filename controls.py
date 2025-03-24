import pyautogui
import time

def attack_enemy(position):
    if position:
        pyautogui.moveTo(position[0], position[1])
        pyautogui.mouseDown()
        time.sleep(0.5)
        pyautogui.mouseUp()
        time.sleep(0.1)

def pickup_loot(position):
    if position:
        pyautogui.moveTo(position[0], position[1])
        pyautogui.mouseDown()
        time.sleep(0.1)
        pyautogui.mouseUp()
        time.sleep(0.1)
