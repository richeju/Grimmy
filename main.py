import detection
import controls
import keyboard
import time

def run_bot():
    print("Bot démarré. Appuie sur 'q' pour quitter.")
    time.sleep(3)  # Délai pour lancer le jeu
    
    while not keyboard.is_pressed('q'):
        enemy_pos = detection.find_enemy()
        if enemy_pos:
            controls.attack_enemy(enemy_pos)
            controls.pickup_loot()
        time.sleep(0.1)  # Réduire la charge CPU
    
    print("Bot arrêté.")

if __name__ == "__main__":
    run_bot()
