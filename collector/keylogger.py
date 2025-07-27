import json
import os
import sys
from pynput import keyboard
from datetime import datetime

# Ruta donde se guardarán los datos
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'profiles', 'keystrokes.json')

keystrokes = []

STOP_KEY = keyboard.Key.f12  # Tecla para detener el keylogger

def save_and_exit():
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(keystrokes, f, ensure_ascii=False, indent=2)
    print(f"\n[INFO] Keystrokes guardados en {DATA_PATH}")
    print("[INFO] Keylogger finalizado.")
    sys.exit(0)

def on_press(key):
    event = {
        'event': 'down',
        'key': str(key),
        'timestamp': datetime.now().isoformat()
    }
    keystrokes.append(event)
    if key == STOP_KEY:
        save_and_exit()

def on_release(key):
    event = {
        'event': 'up',
        'key': str(key),
        'timestamp': datetime.now().isoformat()
    }
    keystrokes.append(event)

if __name__ == "__main__":
    print("[INFO] Keylogger iniciado. Presiona F12 para detener y guardar.")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
