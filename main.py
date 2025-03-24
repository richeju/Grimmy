import detection
import controls
import keyboard
import time
import pyautogui

# Activer le Fail-Safe de pyautogui
pyautogui.FAILSAFE = True  # Déplace la souris en haut à gauche pour arrêter
pyautogui.PAUSE = 0.1  # Petite pause entre les actions

# Obtenir la résolution de l’écran
screen_width, screen_height = pyautogui.size()
center_x, center_y = screen_width // 2, screen_height // 2

def run_bot():
    print("Bot démarré. Déplace la souris en haut à gauche pour arrêter (Fail-Safe).")
    print(f"Résolution détectée : {screen_width}x{screen_height}")
    time.sleep(3)
    
    current_target = None
    
    while not keyboard.is_pressed('q'):  # Garde la condition pour compatibilité
        enemy_positions = detection.find_enemy()
        
        if enemy_positions:
            if not current_target or not any(
                ((pos[0] - current_target[0])**2 + (pos[1] - current_target[1])**2)**0.5 < 50
                for pos in enemy_positions
            ):
                current_target = enemy_positions[0]
            print(f"Cible suivie à {current_target}")
            controls.attack_enemy(current_target)
            controls.pickup_loot(current_target)
        else:
            print("Aucun ennemi détecté, recherche...")
            current_target = None
            pyautogui.moveTo(center_x, center_y - 200)
            pyautogui.dragRel(screen_width // 6, 0, duration=0.5)
        
        time.sleep(0.05)
    
    print("Bot arrêté.")

if __name__ == "__main__":
    run_bot()
