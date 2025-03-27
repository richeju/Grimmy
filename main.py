import detection
import controls
import keyboard
import time
import pyautogui
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
    try:
        windows = gw.getWindowsWithTitle("Grim Dawn")
        if windows:
            grim_dawn_window = windows[0]
            grim_dawn_window.activate()
            time.sleep(0.5)
            return True
        else:
            print("Fenêtre de Grim Dawn non trouvée.")
            return False
    except Exception as e:
        print(f"Erreur lors de l’activation de la fenêtre : {e}")
        return False

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
    
    while not keyboard.is_pressed('q'):
        if not is_grim_dawn_active():
            print("Grim Dawn n’est pas la fenêtre active, tentative de réactivation...")
            if not activate_grim_dawn():
                print("Impossible de réactiver Grim Dawn, mise en pause...")
                time.sleep(1)
                continue
        
        enemy_positions = detection.find_enemy()
        if enemy_positions:
            print(f"Positions détectées : {enemy_positions}")
        else:
            print("Aucun ennemi détecté, en attente...")
        
        if enemy_positions:
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
            current_target = None
            target_start_time = None
            target_position = None
        
        if farm_cycles >= max_cycles:
            return_to_rift()
            farm_cycles = 0
        
        time.sleep(0.05)
    
    print("Bot arrêté.")

if __name__ == "__main__":
    run_bot()
