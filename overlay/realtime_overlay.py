import sys
import time
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor, QCursor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from collections import Counter, deque
from pynput import keyboard
import json
import os

class ModernOverlayButton(QPushButton):
    def __init__(self, text, color="#4A90E2", hover_color="#357ABD"):
        super().__init__(text)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 12px;
                margin: 3px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: #2E5A8A;
            }}
        """)
        self.setCursor(QCursor(Qt.PointingHandCursor))

class RealtimeOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('KeySculptAI - Overlay en Tiempo Real')
        self.setGeometry(100, 100, 450, 350)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Configurar estilo moderno
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(10, 10, 20, 250), stop:1 rgba(15, 15, 35, 250));
                color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
                border-radius: 15px;
                border: 2px solid #4A90E2;
            }
            QLabel {
                color: #E8F4FD;
                background-color: transparent;
            }
            QFrame {
                background-color: rgba(255, 255, 255, 0.08);
                border: 1px solid #4A90E2;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        
        # Variables para métricas
        self.keystrokes = deque(maxlen=1000)
        self.start_time = time.time()
        self.wpm_window = 20
        self.current_wpm = 0
        self.accuracy = 100
        self.key_frequencies = Counter()
        
        # Variables para precisión
        self.total_keystrokes = 0
        self.backspace_count = 0
        self.corrections = 0
        
        # Layout principal
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Header con título y controles
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        
        # Título
        title = QLabel("👁️ KeySculptAI Overlay")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setStyleSheet("color: #4A90E2;")
        header_layout.addWidget(title)
        
        # Indicador de arrastre
        drag_label = QLabel("⟷")
        drag_label.setFont(QFont("Arial", 16))
        drag_label.setStyleSheet("color: #888;")
        drag_label.setToolTip("Arrastra aquí para mover la ventana")
        header_layout.addWidget(drag_label)
        
        layout.addWidget(header_frame)
        
        # Panel de métricas
        metrics_frame = QFrame()
        metrics_layout = QVBoxLayout(metrics_frame)
        
        # Título de métricas
        metrics_title = QLabel("📊 Métricas en Tiempo Real")
        metrics_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        metrics_title.setStyleSheet("color: #4A90E2; margin-bottom: 5px;")
        metrics_title.setAlignment(Qt.AlignCenter)
        metrics_layout.addWidget(metrics_title)
        
        # Métricas en tiempo real
        metrics_grid = QHBoxLayout()
        
        # WPM
        wpm_container = QFrame()
        wpm_container.setStyleSheet("""
            QFrame {
                background-color: rgba(46, 204, 113, 0.2);
                border: 1px solid #2ECC71;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        wpm_layout = QVBoxLayout(wpm_container)
        
        wpm_title = QLabel("🚀 WPM")
        wpm_title.setFont(QFont("Segoe UI", 10))
        wpm_title.setAlignment(Qt.AlignCenter)
        wpm_layout.addWidget(wpm_title)
        
        self.wpm_label = QLabel("0")
        self.wpm_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.wpm_label.setAlignment(Qt.AlignCenter)
        self.wpm_label.setStyleSheet("color: #2ECC71;")
        wpm_layout.addWidget(self.wpm_label)
        
        metrics_grid.addWidget(wpm_container)
        
        # Precisión
        acc_container = QFrame()
        acc_container.setStyleSheet("""
            QFrame {
                background-color: rgba(155, 89, 182, 0.2);
                border: 1px solid #9B59B6;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        acc_layout = QVBoxLayout(acc_container)
        
        acc_title = QLabel("🎯 Precisión")
        acc_title.setFont(QFont("Segoe UI", 10))
        acc_title.setAlignment(Qt.AlignCenter)
        acc_layout.addWidget(acc_title)
        
        self.accuracy_label = QLabel("100%")
        self.accuracy_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.accuracy_label.setAlignment(Qt.AlignCenter)
        self.accuracy_label.setStyleSheet("color: #9B59B6;")
        acc_layout.addWidget(self.accuracy_label)
        
        metrics_grid.addWidget(acc_container)
        
        metrics_layout.addLayout(metrics_grid)
        layout.addWidget(metrics_frame)
        
        # Canvas para heatmap
        viz_frame = QFrame()
        viz_layout = QVBoxLayout(viz_frame)
        
        viz_title = QLabel("⌨️ Uso de Teclas")
        viz_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        viz_title.setStyleSheet("color: #4A90E2; margin-bottom: 5px;")
        viz_title.setAlignment(Qt.AlignCenter)
        viz_layout.addWidget(viz_title)
        
        self.figure, self.ax = plt.subplots(figsize=(5, 3.5))  # Aumentado de 2.5 a 3.5
        self.figure.patch.set_facecolor('none')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumHeight(250)  # Altura mínima para el canvas
        viz_layout.addWidget(self.canvas)
        
        layout.addWidget(viz_frame)
        
        # Botones de control
        controls_frame = QFrame()
        controls_layout = QHBoxLayout(controls_frame)
        
        self.close_btn = ModernOverlayButton("❌ Cerrar", "#E74C3C", "#C0392B")
        self.close_btn.clicked.connect(self.close)
        controls_layout.addWidget(self.close_btn)
        
        self.minimize_btn = ModernOverlayButton("📌 Minimizar", "#3498DB", "#2980B9")
        self.minimize_btn.clicked.connect(self.showMinimized)
        controls_layout.addWidget(self.minimize_btn)
        
        layout.addWidget(controls_frame)
        
        self.setLayout(layout)
        
        # Iniciar captura de teclado
        self.listener = keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release)
        self.listener.start()
        
        # Timer para actualizar métricas
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_metrics)
        self.timer.start(1000)
        
        # Variables para arrastrar la ventana
        self.dragging = False
        self.offset = None
        
    def enterEvent(self, event):
        self.setCursor(QCursor(Qt.SizeAllCursor))
        
    def leaveEvent(self, event):
        self.setCursor(QCursor(Qt.ArrowCursor))
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()
            
    def mouseMoveEvent(self, event):
        if self.dragging and self.offset:
            self.move(self.pos() + event.pos() - self.offset)
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            
    def on_key_press(self, key):
        timestamp = time.time()
        key_str = str(key).strip("'")
        
        if key == keyboard.Key.backspace:
            self.backspace_count += 1
            self.corrections += 1
        elif len(key_str) == 1 and key_str.isalpha():
            self.total_keystrokes += 1
            self.keystrokes.append({
                'key': key_str.lower(),
                'timestamp': timestamp,
                'event': 'press'
            })
            self.key_frequencies[key_str.lower()] += 1
            
    def on_key_release(self, key):
        timestamp = time.time()
        key_str = str(key).strip("'")
        
        if len(key_str) == 1 and key_str.isalpha():
            self.keystrokes.append({
                'key': key_str.lower(),
                'timestamp': timestamp,
                'event': 'release'
            })
            
    def calculate_accuracy(self):
        if self.total_keystrokes == 0:
            return 100
        accuracy = ((self.total_keystrokes - self.corrections) / self.total_keystrokes) * 100
        return max(0, min(100, round(accuracy, 1)))
            
    def calculate_wpm(self):
        if len(self.keystrokes) < 2:
            return 0
            
        current_time = time.time()
        window_start = current_time - self.wpm_window
        
        letters_in_window = 0
        for event in self.keystrokes:
            if (event['event'] == 'press' and 
                event['timestamp'] >= window_start and 
                len(event['key']) == 1 and event['key'].isalpha()):
                letters_in_window += 1
                
        if letters_in_window == 0:
            return 0
            
        time_minutes = self.wpm_window / 60
        wpm = (letters_in_window / 5) / time_minutes
        return round(wpm, 1)
        
    def update_metrics(self):
        self.current_wpm = self.calculate_wpm()
        self.wpm_label.setText(str(self.current_wpm))
        
        self.accuracy = self.calculate_accuracy()
        self.accuracy_label.setText(f"{self.accuracy}%")
        
        self.update_heatmap()
        
    def update_heatmap(self):
        if not self.key_frequencies:
            return
            
        qwerty = [list('qwertyuiop'), list('asdfghjkl'), list('zxcvbnm')]
        max_len = max(len(row) for row in qwerty)
        
        data = []
        for row in qwerty:
            row_data = [self.key_frequencies.get(k, 0) for k in row] + [0]*(max_len - len(row))
            data.append(row_data)
            
        self.ax.clear()
        
        # Configurar colores para fondo oscuro
        plt.style.use('dark_background')
        im = self.ax.imshow(data, cmap='YlOrRd', vmin=0)
        
        # Mostrar letras con mejor contraste
        for i, row in enumerate(qwerty):
            for j, k in enumerate(row):
                freq = self.key_frequencies.get(k, 0)
                # Color blanco para letras usadas, gris claro para no usadas
                color = 'white' if freq > 0 else '#AAAAAA'
                font_weight = 'bold' if freq > 0 else 'normal'
                self.ax.text(j, i, k.upper(), ha='center', va='center', 
                           color=color, fontsize=10, fontweight=font_weight)
                
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_title('Uso de teclas (tiempo real)', color='white', fontsize=12, fontweight='bold')
        
        # Configurar fondo transparente para que coincida con el overlay
        self.figure.patch.set_facecolor('none')
        self.ax.set_facecolor('none')
        
        # Ajustar el layout para evitar cortes
        self.figure.tight_layout()
        
        self.canvas.draw()
        
    def closeEvent(self, event):
        if self.listener:
            self.listener.stop()
        event.accept()

def main():
    app = QApplication(sys.argv)
    overlay = RealtimeOverlay()
    overlay.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 