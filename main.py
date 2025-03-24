import detection
import controls
import keyboard
import time
import pyautogui

def run_bot():
    print("Bot démarré. Appuie sur 'q' pour quitter.")
    time.sleep(3)  # Délai pour lancer le jeu
    
    current_target = None  # Suivre une cible spécifique
    
    while not keyboard.is_pressed('q'):
        enemy_positions = detection.find_enemy()
        
        if enemy_positions:
            # Si on n’a pas de cible ou si la cible actuelle n’est plus détectée
            if not current_target or not any(
                ((pos[0] - current_target[0])**2 + (pos[1] - current_target[1])**2)**0.5 < 50
                for pos in enemy_positions
            ):
                current_target = enemy_positions[0]  # Choisir la première cible détectée
            print(f"Cible suivie à {current_target}")
            controls.attack_enemy(current_target)
            controls.pickup_loot(current_target)
        else:
            print("Aucun ennemi détecté, recherche...")
            current_target = None
            # Déplacer la souris pour "chercher" (balayer l’écran)
            pyautogui.moveTo(960, 540)  # Centre de l’écran
            pyautogui.dragRel(300, 0, duration=0.5)  # Déplacer la caméra vers la droite
        
        time.sleep(0.05)  # Réduit pour une détection plus fluide
    
    print("Bot arrêté.")

if __name__ == "__main__":
    run_bot()
