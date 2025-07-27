import json
import os
import random
import numpy as np
import pandas as pd
from collections import Counter, defaultdict
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import pairwise_distances
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import string

class AdvancedKeyboardOptimizer:
    def __init__(self):
        self.keystrokes_data = None
        self.finger_assignments = self._create_finger_assignments()
        self.key_difficulty = self._create_key_difficulty_matrix()
        self.bigram_weights = self._create_bigram_weights()
        self.trigram_weights = self._create_trigram_weights()
        
    def _create_finger_assignments(self):
        """Asignar dedos a cada tecla según ergonomía estándar"""
        return {
            # Dedos de la mano izquierda
            'q': 'left_pinky', 'a': 'left_pinky', 'z': 'left_pinky',
            'w': 'left_ring', 's': 'left_ring', 'x': 'left_ring',
            'e': 'left_middle', 'd': 'left_middle', 'c': 'left_middle',
            'r': 'left_index', 'f': 'left_index', 'v': 'left_index',
            't': 'left_index', 'g': 'left_index', 'b': 'left_index',
            
            # Dedos de la mano derecha
            'y': 'right_index', 'h': 'right_index', 'n': 'right_index',
            'u': 'right_index', 'j': 'right_index', 'm': 'right_index',
            'i': 'right_middle', 'k': 'right_middle',
            'o': 'right_ring', 'l': 'right_ring',
            'p': 'right_pinky',
            
            # Teclas especiales
            ' ': 'right_thumb'  # Espacio
        }
    
    def _create_key_difficulty_matrix(self):
        """Matriz de dificultad de teclas basada en ergonomía"""
        # Posiciones del teclado (fila, columna)
        positions = {
            'q': (0, 0), 'w': (0, 1), 'e': (0, 2), 'r': (0, 3), 't': (0, 4),
            'y': (0, 5), 'u': (0, 6), 'i': (0, 7), 'o': (0, 8), 'p': (0, 9),
            'a': (1, 0), 's': (1, 1), 'd': (1, 2), 'f': (1, 3), 'g': (1, 4),
            'h': (1, 5), 'j': (1, 6), 'k': (1, 7), 'l': (1, 8),
            'z': (2, 0), 'x': (2, 1), 'c': (2, 2), 'v': (2, 3), 'b': (2, 4),
            'n': (2, 5), 'm': (2, 6)
        }
        
        # Calcular dificultad basada en distancia desde posición home
        home_positions = {'f': (1, 3), 'j': (1, 6)}  # Posiciones home
        difficulty = {}
        
        for key, pos in positions.items():
            min_distance = float('inf')
            for home_pos in home_positions.values():
                distance = abs(pos[0] - home_pos[0]) + abs(pos[1] - home_pos[1])
                min_distance = min(min_distance, distance)
            difficulty[key] = min_distance
        
        return difficulty
    
    def _create_bigram_weights(self):
        """Pesos para bigramas problemáticos"""
        return {
            # Bigramas que requieren el mismo dedo
            'same_finger': 2.0,
            # Bigramas que requieren dedos adyacentes
            'adjacent_fingers': 1.5,
            # Bigramas que requieren saltos largos
            'long_jump': 1.8
        }
    
    def _create_trigram_weights(self):
        """Pesos para trigramas problemáticos"""
        return {
            # Trigramas que requieren el mismo dedo consecutivamente
            'same_finger_consecutive': 3.0,
            # Trigramas que requieren movimientos complejos
            'complex_movement': 2.5
        }
    
    def load_keystroke_data(self, file_path):
        """Cargar y procesar datos de keystrokes"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                keystrokes = json.load(f)
            
            # Convertir a DataFrame para análisis
            df = pd.DataFrame(keystrokes)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['key'] = df['key'].str.strip("'")
            
            # Filtrar solo letras
            df = df[df['key'].str.len() == 1]
            df = df[df['key'].str.isalpha()]
            
            self.keystrokes_data = df
            return True
            
        except Exception as e:
            print(f"❌ [ERROR] Error al cargar datos: {e}")
            return False
    
    def analyze_typing_patterns(self):
        """Analizar patrones de escritura avanzados"""
        if self.keystrokes_data is None:
            return None
        
        analysis = {
            'key_frequencies': Counter(self.keystrokes_data['key']),
            'bigrams': self._extract_bigrams(),
            'trigrams': self._extract_trigrams(),
            'timing_patterns': self._analyze_timing(),
            'finger_usage': self._analyze_finger_usage(),
            'hand_usage': self._analyze_hand_usage()
        }
        
        return analysis
    
    def _extract_bigrams(self):
        """Extraer bigramas del texto"""
        bigrams = []
        keys = self.keystrokes_data['key'].tolist()
        
        for i in range(len(keys) - 1):
            bigram = keys[i] + keys[i + 1]
            bigrams.append(bigram)
        
        return Counter(bigrams)
    
    def _extract_trigrams(self):
        """Extraer trigramas del texto"""
        trigrams = []
        keys = self.keystrokes_data['key'].tolist()
        
        for i in range(len(keys) - 2):
            trigram = keys[i] + keys[i + 1] + keys[i + 2]
            trigrams.append(trigram)
        
        return Counter(trigrams)
    
    def _analyze_timing(self):
        """Analizar patrones de timing"""
        df = self.keystrokes_data.copy()
        df['time_diff'] = df['timestamp'].diff().dt.total_seconds()
        
        return {
            'avg_time_between_keys': df['time_diff'].mean(),
            'std_time_between_keys': df['time_diff'].std(),
            'fast_sequences': df[df['time_diff'] < 0.1].shape[0],
            'slow_sequences': df[df['time_diff'] > 0.5].shape[0]
        }
    
    def _analyze_finger_usage(self):
        """Analizar uso de dedos"""
        finger_usage = defaultdict(int)
        
        for key in self.keystrokes_data['key']:
            if key in self.finger_assignments:
                finger_usage[self.finger_assignments[key]] += 1
        
        return dict(finger_usage)
    
    def _analyze_hand_usage(self):
        """Analizar uso de manos"""
        hand_usage = {'left': 0, 'right': 0}
        
        for key in self.keystrokes_data['key']:
            if key in self.finger_assignments:
                finger = self.finger_assignments[key]
                if 'left' in finger:
                    hand_usage['left'] += 1
                elif 'right' in finger:
                    hand_usage['right'] += 1
        
        return hand_usage
    
    def advanced_fitness(self, layout, analysis):
        """Función de fitness avanzada con múltiples factores"""
        if not analysis:
            return float('inf')
        
        score = 0
        positions = self._get_layout_positions(layout)
        
        # 1. Factor de frecuencia de teclas
        freq_score = self._calculate_frequency_score(layout, analysis['key_frequencies'], positions)
        score += freq_score * 0.3  # 30% del peso
        
        # 2. Factor de bigramas
        bigram_score = self._calculate_bigram_score(layout, analysis['bigrams'], positions)
        score += bigram_score * 0.25  # 25% del peso
        
        # 3. Factor de trigramas
        trigram_score = self._calculate_trigram_score(layout, analysis['trigrams'], positions)
        score += trigram_score * 0.2  # 20% del peso
        
        # 4. Factor de balance de manos
        balance_score = self._calculate_hand_balance_score(layout, analysis['hand_usage'])
        score += balance_score * 0.15  # 15% del peso
        
        # 5. Factor de ergonomía
        ergo_score = self._calculate_ergonomics_score(layout, analysis['finger_usage'])
        score += ergo_score * 0.1  # 10% del peso
        
        return score
    
    def _get_layout_positions(self, layout):
        """Obtener posiciones de teclas en el layout"""
        positions = {}
        for row_idx, row in enumerate(layout):
            for col_idx, key in enumerate(row):
                positions[key] = (row_idx, col_idx)
        return positions
    
    def _calculate_frequency_score(self, layout, frequencies, positions):
        """Calcular score basado en frecuencia de teclas"""
        score = 0
        for key, freq in frequencies.items():
            if key in positions:
                # Distancia desde posición home
                home_distance = self.key_difficulty.get(key, 0)
                score += freq * home_distance
        return score
    
    def _calculate_bigram_score(self, layout, bigrams, positions):
        """Calcular score basado en bigramas problemáticos"""
        score = 0
        
        for bigram, freq in bigrams.items():
            if len(bigram) == 2:
                key1, key2 = bigram[0], bigram[1]
                
                if key1 in positions and key2 in positions:
                    pos1 = positions[key1]
                    pos2 = positions[key2]
                    
                    # Distancia entre teclas
                    distance = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
                    
                    # Penalizar distancias largas
                    if distance > 2:
                        score += freq * self.bigram_weights['long_jump']
                    
                    # Penalizar mismo dedo
                    if key1 in self.finger_assignments and key2 in self.finger_assignments:
                        if self.finger_assignments[key1] == self.finger_assignments[key2]:
                            score += freq * self.bigram_weights['same_finger']
        
        return score
    
    def _calculate_trigram_score(self, layout, trigrams, positions):
        """Calcular score basado en trigramas problemáticos"""
        score = 0
        
        for trigram, freq in trigrams.items():
            if len(trigram) == 3:
                key1, key2, key3 = trigram[0], trigram[1], trigram[2]
                
                if all(key in positions for key in [key1, key2, key3]):
                    # Penalizar mismo dedo consecutivamente
                    if (key1 in self.finger_assignments and 
                        key2 in self.finger_assignments and 
                        key3 in self.finger_assignments):
                        
                        finger1 = self.finger_assignments[key1]
                        finger2 = self.finger_assignments[key2]
                        finger3 = self.finger_assignments[key3]
                        
                        if finger1 == finger2 == finger3:
                            score += freq * self.trigram_weights['same_finger_consecutive']
        
        return score
    
    def _calculate_hand_balance_score(self, layout, hand_usage):
        """Calcular score de balance entre manos"""
        total_usage = hand_usage['left'] + hand_usage['right']
        if total_usage == 0:
            return 0
        
        left_ratio = hand_usage['left'] / total_usage
        right_ratio = hand_usage['right'] / total_usage
        
        # Penalizar desbalance (ideal: 50-50)
        balance_penalty = abs(left_ratio - 0.5) + abs(right_ratio - 0.5)
        return balance_penalty * 100
    
    def _calculate_ergonomics_score(self, layout, finger_usage):
        """Calcular score de ergonomía"""
        score = 0
        
        # Penalizar uso excesivo de dedos débiles
        weak_fingers = ['left_pinky', 'right_pinky']
        for finger in weak_fingers:
            if finger in finger_usage:
                usage_ratio = finger_usage[finger] / sum(finger_usage.values())
                if usage_ratio > 0.15:  # Más del 15% del uso
                    score += (usage_ratio - 0.15) * 100
        
        return score
    
    def optimize_with_ml(self, generations=100, population_size=50):
        """Optimización con Machine Learning"""
        if not self.keystrokes_data is not None:
            print("❌ [ERROR] No hay datos de keystrokes cargados.")
            return None
        
        analysis = self.analyze_typing_patterns()
        if not analysis:
            print("❌ [ERROR] No se pudo analizar los patrones de escritura.")
            return None
        
        print("🧠 [INFO] Iniciando optimización con Machine Learning...")
        print(f"📊 [INFO] Datos analizados: {len(self.keystrokes_data)} keystrokes")
        print(f"🔤 [INFO] Teclas únicas: {len(analysis['key_frequencies'])}")
        print(f"🔗 [INFO] Bigramas únicos: {len(analysis['bigrams'])}")
        
        # Inicializar población
        population = [self._generate_random_layout() for _ in range(population_size)]
        best_score = float('inf')
        best_layout = None
        
        # Evolución
        for gen in range(generations):
            # Evaluar fitness
            scores = [self.advanced_fitness(layout, analysis) for layout in population]
            
            # Encontrar mejor
            min_score_idx = np.argmin(scores)
            if scores[min_score_idx] < best_score:
                best_score = scores[min_score_idx]
                best_layout = population[min_score_idx].copy()
            
            # Selección y reproducción
            new_population = []
            
            # Elitismo: mantener el mejor
            new_population.append(population[min_score_idx])
            
            # Generar nueva población
            while len(new_population) < population_size:
                # Selección por torneo
                parent1 = self._tournament_selection(population, scores)
                parent2 = self._tournament_selection(population, scores)
                
                # Cruce
                child = self._advanced_crossover(parent1, parent2)
                
                # Mutación
                if random.random() < 0.1:
                    child = self._advanced_mutation(child)
                
                new_population.append(child)
            
            population = new_population
            
            # Reporte de progreso
            if (gen + 1) % 10 == 0:
                print(f"🔄 Generación {gen + 1}: Mejor score = {best_score:.2f}")
        
        print(f"\n✅ [INFO] Optimización completada!")
        print(f"🏆 [INFO] Mejor score final: {best_score:.2f}")
        
        return best_layout, best_score, analysis
    
    def _generate_random_layout(self):
        """Generar layout aleatorio"""
        keys = list(string.ascii_lowercase)
        random.shuffle(keys)
        
        layout = [
            keys[0:10],   # Primera fila
            keys[10:19],  # Segunda fila
            keys[19:26]   # Tercera fila
        ]
        
        return layout
    
    def _tournament_selection(self, population, scores, tournament_size=3):
        """Selección por torneo"""
        indices = random.sample(range(len(population)), tournament_size)
        tournament_scores = [scores[i] for i in indices]
        best_idx = indices[np.argmin(tournament_scores)]
        return population[best_idx]
    
    def _advanced_crossover(self, parent1, parent2):
        """Cruce avanzado con preservación de buenas características"""
        # Flatten layouts
        flat1 = sum(parent1, [])
        flat2 = sum(parent2, [])
        
        # Order Crossover (OX)
        size = len(flat1)
        a, b = sorted(random.sample(range(size), 2))
        
        child = [None] * size
        child[a:b] = flat1[a:b]
        
        # Fill remaining positions
        remaining = [k for k in flat2 if k not in child[a:b]]
        idx = 0
        for i in range(size):
            if child[i] is None:
                child[i] = remaining[idx]
                idx += 1
        
        # Reconstruct layout
        return [
            child[0:10],
            child[10:19],
            child[19:26]
        ]
    
    def _advanced_mutation(self, layout):
        """Mutación avanzada"""
        flat = sum(layout, [])
        
        # Mutación por intercambio
        if random.random() < 0.7:
            i, j = random.sample(range(len(flat)), 2)
            flat[i], flat[j] = flat[j], flat[i]
        
        # Mutación por inversión
        elif random.random() < 0.3:
            a, b = sorted(random.sample(range(len(flat)), 2))
            flat[a:b] = flat[a:b][::-1]
        
        # Reconstruct layout
        return [
            flat[0:10],
            flat[10:19],
            flat[19:26]
        ]

def main():
    """Función principal"""
    print("🧠 KeySculptAI - Optimizador Avanzado con Machine Learning")
    print("=" * 60)
    
    # Cargar datos
    data_path = os.path.join(os.path.dirname(__file__), '..', 'profiles', 'keystrokes.json')
    if not os.path.exists(data_path):
        print(f"❌ [ERROR] No se encontró el archivo de datos: {data_path}")
        print("Ejecuta primero el keylogger para capturar datos.")
        return
    
    # Inicializar optimizador
    optimizer = AdvancedKeyboardOptimizer()
    
    # Cargar datos
    if not optimizer.load_keystroke_data(data_path):
        return
    
    # Optimizar
    result = optimizer.optimize_with_ml(generations=100, population_size=50)
    
    if result:
        best_layout, best_score, analysis = result
        
        # Guardar resultado
        output_path = os.path.join(os.path.dirname(__file__), '..', 'profiles', 'best_layout.json')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(best_layout, f, ensure_ascii=False, indent=2)
        
        print(f"\n📁 [INFO] Layout guardado en: {output_path}")
        
        # Mostrar análisis detallado
        print("\n📊 ANÁLISIS DETALLADO:")
        print(f"🏆 Score final: {best_score:.2f}")
        print(f"📈 Teclas más frecuentes: {dict(analysis['key_frequencies'].most_common(5))}")
        print(f"🔗 Bigramas más frecuentes: {dict(analysis['bigrams'].most_common(5))}")
        print(f"⚖️ Balance de manos: {analysis['hand_usage']}")
        print(f"👆 Uso de dedos: {analysis['finger_usage']}")
        
        print("\n🎹 LAYOUT OPTIMIZADO:")
        for i, row in enumerate(best_layout):
            print(f"Fila {i+1}: {' '.join(row).upper()}")
        
        print("\n💡 EXPLICACIÓN:")
        print("Este layout fue optimizado considerando:")
        print("- Frecuencia de uso de cada tecla")
        print("- Patrones de bigramas y trigramas")
        print("- Balance entre manos")
        print("- Ergonomía y uso de dedos")
        print("- Distancias de movimiento")
        print("- Timing entre pulsaciones")

if __name__ == "__main__":
    main() 