import detection
import controls
import keyboard
import time
import pyautogui

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

screen_width, screen_height = pyautogui.size()
center_x, center_y = screen_width // 2, screen_height // 2

def run_bot():
    print("Bot démarré. Déplace la souris en haut à gauche pour arrêter (Fail-Safe).")
    print(f"Résolution détectée : {screen_width}x{screen_height}")
    time.sleep(3)
    
    current_target = None
    target_start_time = None  # Temps où la cible a été détectée
    target_position = None  # Dernière position de la cible
    max_target_duration = 5  # Durée max (en secondes) avant d’ignorer une cible statique
    
    while not keyboard.is_pressed('q'):
        enemy_positions = detection.find_enemy()
        
        if enemy_positions:
            # Vérifier si la cible actuelle est toujours détectée
            if current_target and any(
                ((pos[0] - current_target[0])**2 + (pos[1] - current_target[1])**2)**0.5 < 50
                for pos in enemy_positions
            ):
                # Cible toujours là, vérifier si elle est statique
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
                # Nouvelle cible
                current_target = enemy_positions[0]
                target_start_time = time.time()
                target_position = current_target
            
            if current_target:
                print(f"Cible suivie à {current_target}")
                controls.attack_enemy(current_target)
                controls.pickup_loot(current_target)
        else:
            print("Aucun ennemi détecté, recherche...")
            current_target = None
            target_start_time = None
            target_position = None
            pyautogui.moveTo(center_x, center_y - 200)
            pyautogui.dragRel(screen_width // 6, 0, duration=0.5)
        
        time.sleep(0.05)
    
    print("Bot arrêté.")

if __name__ == "__main__":
    run_bot()
