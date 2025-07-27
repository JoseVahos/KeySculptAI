import json
import os
import random
import string
from collections import Counter

# --- Configuración ---
# Definimos las teclas a optimizar (ejemplo: letras minúsculas)
KEYS = list(string.ascii_lowercase)
# Layout base: filas del teclado QWERTY (puedes ajustar a tu preferencia)
QWERTY_LAYOUT = [
    list('qwertyuiop'),
    list('asdfghjkl'),
    list('zxcvbnm')
]
POP_SIZE = 20
GENERATIONS = 50
TOURNAMENT_SIZE = 3
MUTATION_RATE = 0.2
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), '..', 'profiles', 'best_layout.json')

# Coordenadas de cada tecla en el layout (para calcular distancia)
def get_key_positions(layout):
    positions = {}
    for row_idx, row in enumerate(layout):
        for col_idx, key in enumerate(row):
            positions[key] = (row_idx, col_idx)
    return positions

# Cargar frecuencias de teclas desde el analizador (puedes adaptar el path)
def load_key_frequencies(path):
    with open(path, 'r', encoding='utf-8') as f:
        keystrokes = json.load(f)
    keys = [k['key'].strip("'") for k in keystrokes if k['event'] == 'down' and k['key'].startswith("'") and len(k['key']) == 3]
    return Counter(keys)

# Función de fitness: suma ponderada de (frecuencia * distancia desde la posición "óptima")
def fitness(layout, freq_counter, ref_positions):
    positions = get_key_positions(layout)
    score = 0
    for key, freq in freq_counter.items():
        if key in positions and key in ref_positions:
            # Distancia Manhattan entre la posición actual y la "óptima" (QWERTY)
            d = abs(positions[key][0] - ref_positions[key][0]) + abs(positions[key][1] - ref_positions[key][1])
            score += freq * d
    return score  # Menor es mejor

# Generar un layout aleatorio
def random_layout():
    keys = KEYS.copy()
    random.shuffle(keys)
    # Asignar a filas como en QWERTY
    layout = []
    idx = 0
    for row in QWERTY_LAYOUT:
        layout.append(keys[idx:idx+len(row)])
        idx += len(row)
    return layout

def crossover(parent1, parent2):
    # Cruce de orden (Order Crossover, OX)
    flat1 = sum(parent1, [])
    flat2 = sum(parent2, [])
    size = len(flat1)
    a, b = sorted(random.sample(range(size), 2))
    child = [None]*size
    child[a:b] = flat1[a:b]
    fill = [k for k in flat2 if k not in child[a:b]]
    idx = 0
    for i in range(size):
        if child[i] is None:
            child[i] = fill[idx]
            idx += 1
    # Reconstruir en filas
    out = []
    idx = 0
    for row in QWERTY_LAYOUT:
        out.append(child[idx:idx+len(row)])
        idx += len(row)
    return out

def mutate(layout):
    # Mutación: intercambiar dos teclas aleatorias
    flat = sum(layout, [])
    i, j = random.sample(range(len(flat)), 2)
    flat[i], flat[j] = flat[j], flat[i]
    # Reconstruir
    out = []
    idx = 0
    for row in QWERTY_LAYOUT:
        out.append(flat[idx:idx+len(row)])
        idx += len(row)
    return out

def tournament_selection(population, scores):
    selected = random.sample(list(zip(population, scores)), TOURNAMENT_SIZE)
    selected.sort(key=lambda x: x[1])
    return selected[0][0]

# --- Esqueleto del ciclo evolutivo ---
def main():
    # Cargar frecuencias de teclas
    freq_path = os.path.join(os.path.dirname(__file__), '..', 'profiles', 'keystrokes.json')
    if not os.path.exists(freq_path):
        print(f"[ERROR] No se encontró el archivo de datos: {freq_path}")
        print("Ejecuta primero el keylogger para capturar datos.")
        return
    freq_counter = load_key_frequencies(freq_path)
    # Layout de referencia (QWERTY)
    ref_positions = get_key_positions(QWERTY_LAYOUT)
    # Inicializar población
    population = [random_layout() for _ in range(POP_SIZE)]
    for gen in range(GENERATIONS):
        scores = [fitness(layout, freq_counter, ref_positions) for layout in population]
        new_population = []
        # Elitismo: conservar el mejor
        best_idx = scores.index(min(scores))
        new_population.append(population[best_idx])
        while len(new_population) < POP_SIZE:
            parent1 = tournament_selection(population, scores)
            parent2 = tournament_selection(population, scores)
            child = crossover(parent1, parent2)
            if random.random() < MUTATION_RATE:
                child = mutate(child)
            new_population.append(child)
        population = new_population
        if (gen+1) % 10 == 0 or gen == 0:
            print(f"Generación {gen+1}: Mejor score = {min(scores)}")
    # Layout final
    final_scores = [fitness(layout, freq_counter, ref_positions) for layout in population]
    best_idx = final_scores.index(min(final_scores))
    best_layout = population[best_idx]
    print("\nMejor layout encontrado:")
    for row in best_layout:
        print(' '.join(row))
    print(f"Score: {final_scores[best_idx]}")
    # Guardar layout
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(best_layout, f, ensure_ascii=False, indent=2)
    print(f"\n[INFO] Layout guardado en {OUTPUT_PATH}")

    # --- Explicación del resultado ---
    print("\n--- EXPLICACIÓN DEL RESULTADO ---")
    print("El score representa el esfuerzo total estimado para escribir con este layout, basado en:")
    print("- La frecuencia de cada letra en tus datos de escritura.")
    print("- La distancia Manhattan entre la posición de cada letra en el layout final y su posición en QWERTY.")
    print("Un score menor indica que las letras más usadas están más cerca de sus posiciones óptimas (o de fácil acceso).\n")
    # Mostrar las 5 letras más frecuentes y su posición en el layout final
    print("Teclas más frecuentes y su posición en el layout personalizado:")
    freq_sorted = sorted(freq_counter.items(), key=lambda x: -x[1])
    positions = get_key_positions(best_layout)
    for key, freq in freq_sorted[:5]:
        pos = positions.get(key, None)
        if pos:
            print(f"  '{key}': fila {pos[0]+1}, columna {pos[1]+1} (usada {freq} veces)")
        else:
            print(f"  '{key}': no está en el layout")
    print("\nEste layout fue seleccionado porque minimiza el esfuerzo total según tu estilo de escritura registrado.")

if __name__ == "__main__":
    main()
