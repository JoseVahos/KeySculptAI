import json
import os
from collections import Counter
from datetime import datetime

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'profiles', 'keystrokes.json')

def load_keystrokes():
    if not os.path.exists(DATA_PATH):
        print(f"[ERROR] No se encontró el archivo de datos: {DATA_PATH}")
        print("Ejecuta primero el keylogger para capturar datos.")
        return None
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def calc_wpm(keystrokes):
    letters = [k for k in keystrokes if k['event'] == 'down' and k['key'].startswith("'" ) and len(k['key']) == 3]
    if not letters:
        return 0
    t0 = datetime.fromisoformat(letters[0]['timestamp'])
    t1 = datetime.fromisoformat(letters[-1]['timestamp'])
    elapsed_min = (t1 - t0).total_seconds() / 60
    if elapsed_min == 0:
        return 0
    wpm = len(letters) / 5 / elapsed_min
    return round(wpm, 2)

def key_frequencies(keystrokes):
    keys = [k['key'] for k in keystrokes if k['event'] == 'down']
    return Counter(keys)

def avg_time_between_presses(keystrokes):
    downs = [k for k in keystrokes if k['event'] == 'down']
    if len(downs) < 2:
        return 0
    times = [datetime.fromisoformat(k['timestamp']) for k in downs]
    deltas = [(t2 - t1).total_seconds() for t1, t2 in zip(times, times[1:])]
    return round(sum(deltas) / len(deltas), 3)

def main():
    keystrokes = load_keystrokes()
    if keystrokes is None:
        return
    print(f"Total de eventos: {len(keystrokes)}")
    print(f"WPM estimado: {calc_wpm(keystrokes)}")
    print(f"Tiempo promedio entre pulsaciones: {avg_time_between_presses(keystrokes)} s")
    print("Frecuencia de teclas (top 10):")
    for key, freq in key_frequencies(keystrokes).most_common(10):
        print(f"  {key}: {freq}")

if __name__ == "__main__":
    main()
