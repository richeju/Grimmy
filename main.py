import detection
import controls
import keyboard
import time
import pyautogui
import cv2
import numpy as np
import pygetwindow as gw

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

screen_width, screen_height = pyautogui.size()
center_x, center_y = screen_width // 2, screen_height // 2

def is_grim_dawn_active():
    try:
        active_window = gw.getActiveWindow()
        if active_window and "Grim Dawn" in active_window.title:
            return True
        return False
    except Exception as e:
        print(f"Erreur lors de la vérification de la fenêtre : {e}")
        return False

def activate_grim_dawn():
    """Réactiver la fenêtre de Grim Dawn si elle n’est pas active."""
    try:
        windows = gw.getWindowsWithTitle("Grim Dawn")
        if windows:
            grim_dawn_window = windows[0]
            grim_dawn_window.activate()
            time.sleep(0.5)  # Attendre que la fenêtre soit active
            return True
        else:
            print("Fenêtre de Grim Dawn non trouvée.")
            return False
    except Exception as e:
        print(f"Erreur lors de l’activation de la fenêtre : {e}")
        return False

def find_quest_marker():
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2HSV)
    
    lower_green = np.array([35, 100, 100])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(screenshot, lower_green, upper_green)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) > 50:
            x, y, w, h = cv2.boundingRect(contour)
            if 10 < w < 50 and 10 < h < 50:
                # Vérifier que la position est dans une zone "sûre" (pas près des bords)
                marker_x, marker_y = x + w // 2, y + h // 2
                if 100 < marker_x < screen_width - 100 and 100 < marker_y < screen_height - 100:
                    return (marker_x, marker_y)
    return None

def find_npc_marker():
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2HSV)
    
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    mask = cv2.inRange(screenshot, lower_yellow, upper_yellow)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) > 50:
            x, y, w, h = cv2.boundingRect(contour)
            if 10 < w < 50 and 10 < h < 50:
                # Vérifier que la position est dans une zone "sûre"
                marker_x, marker_y = x + w // 2, y + h // 2
                if 100 < marker_x < screen_width - 100 and 100 < marker_y < screen_height - 100:
                    return (marker_x, marker_y)
    return None

def return_to_rift():
    print("Retour à la faille...")
    pyautogui.press('t')
    time.sleep(0.5)
    pyautogui.click(center_x, center_y)
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(5)

def run_bot():
    print("Bot démarré. Déplace la souris en haut à gauche pour arrêter (Fail-Safe).")
    print(f"Résolution détectée : {screen_width}x{screen_height}")
    time.sleep(3)
    
    current_target = None
    target_start_time = None
    target_position = None
    max_target_duration = 5
    farm_cycles = 0
    max_cycles = 5
    search_mode = False
    search_direction = 1
    search_counter = 0
    
    while not keyboard.is_pressed('q'):
        # Vérifier si Grim Dawn est actif, sinon le réactiver
        if not is_grim_dawn_active():
            print("Grim Dawn n’est pas la fenêtre active, tentative de réactivation...")
            if not activate_grim_dawn():
                print("Impossible de réactiver Grim Dawn, mise en pause...")
                time.sleep(1)
                continue
        
        enemy_positions = detection.find_enemy()
        
        if enemy_positions:
            search_mode = False
            search_counter = 0
            if current_target and any(
                ((pos[0] - current_target[0])**2 + (pos[1] - current_target[1])**2)**0.5 < 50
                for pos in enemy_positions
            ):
                if target_position == current_target:
                    if time.time() - target_start_time > max_target_duration:
                        print("Cible statique détectée (probablement pas un ennemi), changement de cible...")
                        current_target = None
                        target_start_time = None
                        target_position = None
                else:
                    target_position = current_target
                    target_start_time = time.time()
            else:
                current_target = enemy_positions[0]
                target_start_time = time.time()
                target_position = current_target
            
            if current_target:
                print(f"Cible suivie à {current_target}")
                controls.attack_enemy(current_target)
                controls.pickup_loot(current_target)
                farm_cycles += 1
        else:
            print("Aucun ennemi détecté, recherche d’une quête ou déplacement...")
            current_target = None
            target_start_time = None
            target_position = None
            
            npc_marker = find_npc_marker()
            if npc_marker:
                print(f"PNJ détecté à {npc_marker}")
                pyautogui.moveTo(npc_marker[0], npc_marker[1])
                pyautogui.mouseDown()
                time.sleep(0.1)
                pyautogui.mouseUp()
                time.sleep(1)
                pyautogui.moveTo(center_x, center_y)
                pyautogui.mouseDown()
                time.sleep(0.1)
                pyautogui.mouseUp()
                time.sleep(0.5)
            else:
                quest_marker = find_quest_marker()
                if quest_marker:
                    print(f"Flèche de quête détectée à {quest_marker}")
                    pyautogui.moveTo(quest_marker[0], quest_marker[1])
                    pyautogui.mouseDown()
                    time.sleep(0.1)
                    pyautogui.mouseUp()
                else:
                    search_mode = True
                    print("Mode recherche activé...")
                    pyautogui.keyDown('w')
                    time.sleep(0.5)
                    pyautogui.keyUp('w')
                    search_counter += 1
                    if search_counter >= 3:
                        pyautogui.moveTo(center_x, center_y - 200)
                        pyautogui.dragRel((screen_width // 8) * search_direction, 0, duration=0.3)
                        search_direction *= -1
                        search_counter = 0
        
        if farm_cycles >= max_cycles:
            return_to_rift()
            farm_cycles = 0
            search_mode = False
        
        time.sleep(0.05)
    
    print("Bot arrêté.")

if __name__ == "__main__":
    run_bot()
