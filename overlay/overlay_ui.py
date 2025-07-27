import sys
import subprocess
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, 
                             QTextEdit, QMessageBox, QLabel, QHBoxLayout, QGridLayout,
                             QFrame, QSpacerItem, QSizePolicy, QScrollArea)
from PyQt5.QtCore import QProcess, Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QFont, QPalette, QColor, QCursor, QPixmap, QIcon
import os
import traceback
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import json
from collections import Counter

class ModernButton(QPushButton):
    def __init__(self, text, color="#4A90E2", hover_color="#357ABD"):
        super().__init__(text)
        self.color = color
        self.hover_color = hover_color
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 20px;
                font-weight: bold;
                font-size: 14px;
                margin: 5px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: #2E5A8A;
            }}
        """)
        self.setCursor(QCursor(Qt.PointingHandCursor))

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('KeySculptAI - Optimizador de Teclado Inteligente')
        self.setGeometry(100, 100, 1200, 900)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a2e, stop:1 #16213e);
                color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                color: #E8F4FD;
                background-color: transparent;
            }
            QTextEdit {
                background-color: rgba(255, 255, 255, 0.1);
                border: 2px solid #4A90E2;
                border-radius: 10px;
                color: #E8F4FD;
                padding: 10px;
                font-family: 'Consolas', 'Monaco', monospace;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: rgba(255, 255, 255, 0.1);
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #4A90E2;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #357ABD;
            }
        """)
        
        # Layout principal con scroll
        main_scroll = QScrollArea()
        main_scroll.setWidgetResizable(True)
        main_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        main_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Widget contenedor para el contenido
        content_widget = QWidget()
        main_layout = QVBoxLayout(content_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Header con título
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4A90E2, stop:1 #357ABD);
                border-radius: 15px;
                padding: 20px;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        
        title = QLabel("🎹 KeySculptAI")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; margin-bottom: 10px;")
        
        subtitle = QLabel("Optimizador de Teclado Inteligente")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #E8F4FD; opacity: 0.8;")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addWidget(header_frame)
        
        # Panel de controles
        controls_frame = QFrame()
        controls_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.05);
                border: 2px solid #4A90E2;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        controls_layout = QVBoxLayout(controls_frame)
        
        # Botón principal
        self.auto_btn = ModernButton('🚀 Iniciar Análisis Completo', "#2ECC71", "#27AE60")
        self.auto_btn.clicked.connect(self.run_full_pipeline)
        controls_layout.addWidget(self.auto_btn)
        
        # Botones secundarios en grid
        secondary_layout = QGridLayout()
        
        self.capture_btn = ModernButton('📊 Capturar Datos', "#3498DB", "#2980B9")
        self.capture_btn.clicked.connect(self.run_keylogger)
        secondary_layout.addWidget(self.capture_btn, 0, 0)
        
        self.analyze_btn = ModernButton('📈 Analizar Datos', "#9B59B6", "#8E44AD")
        self.analyze_btn.clicked.connect(self.run_analyzer)
        secondary_layout.addWidget(self.analyze_btn, 0, 1)
        
        self.optimize_btn = ModernButton('⚡ Optimizar Layout', "#E67E22", "#D35400")
        self.optimize_btn.clicked.connect(self.run_optimizer)
        
        self.ml_optimize_btn = ModernButton('🧠 Optimizar con ML', "#9B59B6", "#8E44AD")
        self.ml_optimize_btn.clicked.connect(self.run_ml_optimizer)
        secondary_layout.addWidget(self.optimize_btn, 1, 0)
        
        self.overlay_btn = ModernButton('👁️ Lanzar Overlay', "#E74C3C", "#C0392B")
        self.overlay_btn.clicked.connect(self.launch_overlay)
        secondary_layout.addWidget(self.overlay_btn, 1, 1)
        
        self.remapper_btn = ModernButton('🎹 Aplicar Layout', "#F39C12", "#E67E22")
        self.remapper_btn.clicked.connect(self.toggle_remapper)
        secondary_layout.addWidget(self.remapper_btn, 2, 0, 1, 2)  # Span 2 columns
        
        controls_layout.addLayout(secondary_layout)
        main_layout.addWidget(controls_frame)
        
        # Panel de resultados
        results_frame = QFrame()
        results_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.05);
                border: 2px solid #4A90E2;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        results_layout = QVBoxLayout(results_frame)
        
        results_title = QLabel("📋 Resultados y Logs")
        results_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        results_title.setStyleSheet("color: #4A90E2; margin-bottom: 10px;")
        results_layout.addWidget(results_title)
        
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setMinimumHeight(300)  # Aumentado de 200 a 300
        self.output.setMaximumHeight(400)  # Aumentado el máximo también
        results_layout.addWidget(self.output)
        
        main_layout.addWidget(results_frame)
        
        # Panel de visualizaciones
        viz_frame = QFrame()
        viz_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.05);
                border: 2px solid #4A90E2;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        viz_layout = QVBoxLayout(viz_frame)
        
        viz_title = QLabel("📊 Visualizaciones")
        viz_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        viz_title.setStyleSheet("color: #4A90E2; margin-bottom: 10px;")
        viz_layout.addWidget(viz_title)
        
        # Canvas para matplotlib con dos subplots - AUMENTADO EL TAMAÑO
        self.figure, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(12, 6))  # Aumentado de 4 a 6
        self.figure.patch.set_facecolor('none')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumHeight(400)  # Altura mínima para el canvas
        viz_layout.addWidget(self.canvas)
        
        main_layout.addWidget(viz_frame)
        
        # Configurar scroll area
        main_scroll.setWidget(content_widget)
        
        # Layout principal de la ventana
        window_layout = QVBoxLayout(self)
        window_layout.addWidget(main_scroll)
        window_layout.setContentsMargins(0, 0, 0, 0)
        
        # Variables de estado
        self.keylogger_process = None
        self._pipeline_next = None
        self.freq_data = Counter()
        self.overlay_process = None
        self.remapper_process = None
        self.remapping_active = False
        
        # Timer para verificar el estado del remapper
        self.remapper_check_timer = QTimer(self)
        self.remapper_check_timer.timeout.connect(self.check_remapper_status)
        self.remapper_check_timer.start(2000)  # Verificar cada 2 segundos
        
        # Animaciones
        self.setup_animations()

    def setup_animations(self):
        # Animación de entrada para los botones
        self.buttons = [self.auto_btn, self.capture_btn, self.analyze_btn, 
                       self.optimize_btn, self.ml_optimize_btn, self.overlay_btn, self.remapper_btn]
        
        for i, btn in enumerate(self.buttons):
            anim = QPropertyAnimation(btn, b"geometry")
            anim.setDuration(500 + i * 100)
            anim.setStartValue(QRect(btn.x(), btn.y() + 50, btn.width(), btn.height()))
            anim.setEndValue(btn.geometry())
            anim.setEasingCurve(QEasingCurve.OutBack)
            anim.start()

    def launch_overlay(self):
        try:
            overlay_path = os.path.join(os.path.dirname(__file__), 'realtime_overlay.py')
            if self.overlay_process is None or self.overlay_process.state() == QProcess.NotRunning:
                self.overlay_process = QProcess(self)
                self.overlay_process.finished.connect(self.overlay_finished)
                self.overlay_process.start(sys.executable, [overlay_path])
                self.output.append("✅ [INFO] Overlay en tiempo real lanzado.")
                self.overlay_btn.setText("👁️ Overlay Activo")
                self.overlay_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #27AE60;
                        color: white;
                        border: none;
                        border-radius: 12px;
                        padding: 12px 20px;
                        font-weight: bold;
                        font-size: 14px;
                        margin: 5px;
                    }
                    QPushButton:hover {
                        background-color: #2ECC71;
                    }
                """)
            else:
                QMessageBox.information(self, "Overlay", "El overlay ya está en ejecución.")
        except Exception as e:
            self.output.append(f"❌ [ERROR] No se pudo lanzar el overlay: {e}")
            self.output.append(traceback.format_exc())

    def overlay_finished(self):
        # Resetear el botón cuando el overlay se cierra
        self.overlay_btn.setText("👁️ Lanzar Overlay")
        self.overlay_btn.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 20px;
                font-weight: bold;
                font-size: 14px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        self.output.append("ℹ️ [INFO] Overlay en tiempo real cerrado.")
        self.overlay_process = None

    def toggle_remapper(self):
        """Alternar el estado del remapper"""
        if not self.remapping_active:
            self.start_remapper()
        else:
            self.stop_remapper()

    def start_remapper(self):
        """Iniciar el remapper"""
        try:
            remapper_path = os.path.join(os.path.dirname(__file__), '..', 'remapper', 'windows_remap_simple.py')
            
            if not os.path.exists(remapper_path):
                self.output.append("❌ [ERROR] No se encontró el archivo del remapper.")
                return
            
            # Verificar que existe un layout optimizado
            layout_file = os.path.join(os.path.dirname(__file__), '..', 'profiles', 'best_layout.json')
            if not os.path.exists(layout_file):
                self.output.append("❌ [ERROR] No hay layout optimizado disponible.")
                self.output.append("Ejecuta primero el optimizador para generar un layout.")
                return
            
            # Configurar el proceso con mejor manejo
            self.remapper_process = QProcess(self)
            self.remapper_process.setProcessChannelMode(QProcess.MergedChannels)
            self.remapper_process.readyReadStandardOutput.connect(self.handle_remapper_output)
            self.remapper_process.finished.connect(self.remapper_finished)
            self.remapper_process.errorOccurred.connect(self.handle_remapper_error)
            
            # Configurar el entorno para el proceso hijo
            env = self.remapper_process.processEnvironment()
            env.insert("PYTHONUNBUFFERED", "1")  # Evitar buffering de salida
            self.remapper_process.setProcessEnvironment(env)
            
            # Iniciar el proceso
            self.remapper_process.start(sys.executable, [remapper_path])
            
            # Esperar un momento para verificar que el proceso se inició correctamente
            if self.remapper_process.waitForStarted(5000):  # 5 segundos de timeout
                self.remapping_active = True
                self.remapper_btn.setText("🛑 Detener Layout")
                self.remapper_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #E74C3C;
                        color: white;
                        border: none;
                        border-radius: 12px;
                        padding: 12px 20px;
                        font-weight: bold;
                        font-size: 14px;
                        margin: 5px;
                    }
                    QPushButton:hover {
                        background-color: #C0392B;
                    }
                """)
                
                self.output.append("✅ [INFO] Layout optimizado aplicado.")
                self.output.append("💡 [TIP] Presiona F12 en cualquier lugar para detener el remapeo.")
                self.output.append("🔧 [INFO] El remapper está ejecutándose en segundo plano.")
            else:
                self.output.append("❌ [ERROR] El remapper no pudo iniciarse correctamente.")
                self.remapper_process = None
            
        except Exception as e:
            self.output.append(f"❌ [ERROR] No se pudo iniciar el remapper: {e}")
            self.output.append(traceback.format_exc())

    def stop_remapper(self):
        """Detener el remapper"""
        if self.remapper_process and self.remapper_process.state() != QProcess.NotRunning:
            self.output.append("🛑 [INFO] Deteniendo remapper...")
            
            # Intentar terminar suavemente primero
            self.remapper_process.terminate()
            
            # Esperar hasta 3 segundos para que termine suavemente
            if not self.remapper_process.waitForFinished(3000):
                # Si no termina suavemente, forzar la terminación
                self.output.append("⚠️ [WARNING] Forzando terminación del remapper...")
                self.remapper_process.kill()
                self.remapper_process.waitForFinished(1000)
        
        self.remapping_active = False
        self.remapper_btn.setText("🎹 Aplicar Layout")
        self.remapper_btn.setStyleSheet("""
            QPushButton {
                background-color: #F39C12;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 20px;
                font-weight: bold;
                font-size: 14px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #E67E22;
            }
        """)
        
        self.output.append("🛑 [INFO] Layout original restaurado.")
        self.remapper_process = None

    def handle_remapper_output(self):
        """Manejar la salida del remapper"""
        if self.remapper_process:
            data = self.remapper_process.readAllStandardOutput().data().decode()
            if data.strip():
                self.output.append(f"🎹 [REMAPPER] {data.strip()}")

    def handle_remapper_error(self, error):
        """Manejar errores del remapper"""
        error_messages = {
            QProcess.FailedToStart: "No se pudo iniciar el proceso",
            QProcess.Crashed: "El proceso se cerró inesperadamente",
            QProcess.Timedout: "El proceso excedió el tiempo de espera",
            QProcess.WriteError: "Error al escribir en el proceso",
            QProcess.ReadError: "Error al leer del proceso",
            QProcess.UnknownError: "Error desconocido"
        }
        error_msg = error_messages.get(error, f"Error {error}")
        self.output.append(f"❌ [ERROR] Remapper: {error_msg}")
        
        # Si el proceso falló, resetear el estado
        if error in [QProcess.FailedToStart, QProcess.Crashed]:
            self.remapping_active = False
            self.remapper_btn.setText("🎹 Aplicar Layout")
            self.remapper_btn.setStyleSheet("""
                QPushButton {
                    background-color: #F39C12;
                    color: white;
                    border: none;
                    border-radius: 12px;
                    padding: 12px 20px;
                    font-weight: bold;
                    font-size: 14px;
                    margin: 5px;
                }
                QPushButton:hover {
                    background-color: #E67E22;
                }
            """)
            self.remapper_process = None

    def remapper_finished(self, exit_code, exit_status):
        """Manejar cuando el remapper termina"""
        self.remapping_active = False
        self.remapper_btn.setText("🎹 Aplicar Layout")
        self.remapper_btn.setStyleSheet("""
            QPushButton {
                background-color: #F39C12;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 20px;
                font-weight: bold;
                font-size: 14px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #E67E22;
            }
        """)
        
        if exit_status == QProcess.NormalExit:
            self.output.append(f"ℹ️ [INFO] Remapper finalizado normalmente (código: {exit_code}).")
        else:
            self.output.append(f"⚠️ [WARNING] Remapper finalizado con error (código: {exit_code}).")
        
        self.remapper_process = None

    def check_remapper_status(self):
        """Verificar el estado del remapper periódicamente"""
        if self.remapper_process and self.remapping_active:
            if self.remapper_process.state() == QProcess.NotRunning:
                # El proceso se cerró inesperadamente
                self.output.append("⚠️ [WARNING] El remapper se cerró inesperadamente.")
                self.remapping_active = False
                self.remapper_btn.setText("🎹 Aplicar Layout")
                self.remapper_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #F39C12;
                        color: white;
                        border: none;
                        border-radius: 12px;
                        padding: 12px 20px;
                        font-weight: bold;
                        font-size: 14px;
                        margin: 5px;
                    }
                    QPushButton:hover {
                        background-color: #E67E22;
                    }
                """)
                self.remapper_process = None

    def run_keylogger(self):
        if self.keylogger_process is not None:
            QMessageBox.warning(self, "Keylogger", "El keylogger ya está en ejecución.")
            return
        try:
            keylogger_path = os.path.join(os.path.dirname(__file__), '..', 'collector', 'keylogger.py')
            self.keylogger_process = QProcess(self)
            self.keylogger_process.readyReadStandardOutput.connect(self.handle_keylogger_output)
            self.keylogger_process.readyReadStandardError.connect(self.handle_keylogger_output)
            self.keylogger_process.finished.connect(self.keylogger_finished)
            self.keylogger_process.start(sys.executable, [keylogger_path])
            QMessageBox.information(self, "Keylogger", "Keylogger iniciado. Presiona F12 para detener y guardar.")
        except Exception as e:
            self.output.append(f"❌ [ERROR] No se pudo iniciar el keylogger: {e}")
            self.output.append(traceback.format_exc())

    def handle_keylogger_output(self):
        if self.keylogger_process:
            data = self.keylogger_process.readAllStandardOutput().data().decode()
            self.output.append(data)

    def keylogger_finished(self):
        self.keylogger_process = None
        QMessageBox.information(self, "Keylogger", "Keylogger finalizado y datos guardados.")
        if self._pipeline_next:
            self._pipeline_next()

    def run_analyzer(self):
        try:
            analyzer_path = os.path.join(os.path.dirname(__file__), '..', 'collector', 'analyzer.py')
            result = subprocess.run([sys.executable, analyzer_path], capture_output=True, text=True)
            if result.returncode == 0:
                self.output.append("📊 [ANÁLISIS DE DATOS]\n" + result.stdout)
                self.plot_heatmap()
            else:
                self.output.append(f"❌ [ERROR] {result.stderr}")
        except Exception as e:
            self.output.append(f"❌ [ERROR] No se pudo ejecutar el analizador: {e}")
            self.output.append(traceback.format_exc())
        if self._pipeline_next:
            self._pipeline_next()

    def run_optimizer(self):
        try:
            optimizer_path = os.path.join(os.path.dirname(__file__), '..', 'optimizer', 'genetic_optimizer.py')
            result = subprocess.run([sys.executable, optimizer_path], capture_output=True, text=True)
            if result.returncode == 0:
                self.output.append("⚡ [OPTIMIZADOR]\n" + result.stdout)
                self.plot_optimized_layout()
            else:
                self.output.append(f"❌ [ERROR] {result.stderr}")
        except Exception as e:
            self.output.append(f"❌ [ERROR] No se pudo ejecutar el optimizador: {e}")
            self.output.append(traceback.format_exc())
        self._pipeline_next = None

    def run_ml_optimizer(self):
        try:
            ml_optimizer_path = os.path.join(os.path.dirname(__file__), '..', 'optimizer', 'ml_optimizer.py')
            result = subprocess.run([sys.executable, ml_optimizer_path], capture_output=True, text=True)
            if result.returncode == 0:
                self.output.append("🧠 [OPTIMIZADOR ML]\n" + result.stdout)
                self.plot_optimized_layout()
            else:
                self.output.append(f"❌ [ERROR] {result.stderr}")
        except Exception as e:
            self.output.append(f"❌ [ERROR] No se pudo ejecutar el optimizador ML: {e}")
            self.output.append(traceback.format_exc())

    def run_full_pipeline(self):
        self.output.append("🚀 [FLUJO AUTOMÁTICO] Iniciando captura de datos...")
        self._pipeline_next = self._run_analyzer_then_optimizer
        self.run_keylogger()

    def _run_analyzer_then_optimizer(self):
        self._pipeline_next = self.run_optimizer
        self.run_analyzer()

    def on_mouse_move(self, event):
        if event.inaxes in [self.ax1, self.ax2]:
            x, y = int(event.xdata), int(event.ydata)
            if 0 <= y < len(self.current_data) and 0 <= x < len(self.current_data[0]):
                freq = self.current_data[y][x]
                key = self.current_labels[y][x]
                if key and freq > 0:
                    event.inaxes.set_title(f'Tecla: {key.upper()}, Frecuencia: {freq}')
                    self.canvas.draw_idle()

    def plot_heatmap(self):
        freq_path = os.path.join(os.path.dirname(__file__), '..', 'profiles', 'keystrokes.json')
        if not os.path.exists(freq_path):
            self.ax1.clear()
            self.ax1.set_title('No hay datos para mostrar el heatmap')
            self.canvas.draw()
            return
        with open(freq_path, 'r', encoding='utf-8') as f:
            keystrokes = json.load(f)
        keys = [k['key'].strip("'") for k in keystrokes if k['event'] == 'down' and k['key'].startswith("'") and len(k['key']) == 3]
        self.freq_data = Counter(keys)
        qwerty = [list('qwertyuiop'), list('asdfghjkl'), list('zxcvbnm')]
        max_len = max(len(row) for row in qwerty)
        data = []
        label_grid = []
        for row in qwerty:
            row_data = [self.freq_data.get(k, 0) for k in row] + [0]*(max_len - len(row))
            row_labels = [k for k in row] + ['']*(max_len - len(row))
            data.append(row_data)
            label_grid.append(row_labels)
        
        self.ax1.clear()
        # Configurar colores para fondo oscuro
        plt.style.use('dark_background')
        im = self.ax1.imshow(data, cmap='YlOrRd', vmin=0)
        
        for i, row in enumerate(label_grid):
            for j, k in enumerate(row):
                if k:
                    freq = self.freq_data.get(k, 0)
                    color = 'white' if freq > 0 else '#AAAAAA'
                    font_weight = 'bold' if freq > 0 else 'normal'
                    self.ax1.text(j, i, k.upper(), ha='center', va='center', 
                                 color=color, fontsize=12, fontweight=font_weight)
        
        self.ax1.set_xticks([])
        self.ax1.set_yticks([])
        self.ax1.set_title('Heatmap de frecuencias de teclas (QWERTY)\nPasa el mouse sobre las teclas para ver frecuencias', 
                          color='white', fontsize=12, fontweight='bold')
        
        # Configurar fondo transparente
        self.figure.patch.set_facecolor('none')
        self.ax1.set_facecolor('none')
        
        cbar = self.figure.colorbar(im, ax=self.ax1, orientation='vertical', fraction=0.025)
        cbar.ax.tick_params(colors='white')
        
        self.current_data = data
        self.current_labels = label_grid
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.canvas.draw()

    def plot_optimized_layout(self):
        layout_path = os.path.join(os.path.dirname(__file__), '..', 'profiles', 'best_layout.json')
        freq_path = os.path.join(os.path.dirname(__file__), '..', 'profiles', 'keystrokes.json')
        if not os.path.exists(layout_path):
            self.ax2.clear()
            self.ax2.set_title('No hay layout optimizado para mostrar')
            self.canvas.draw()
            return
        with open(layout_path, 'r', encoding='utf-8') as f:
            layout = json.load(f)
        freq = Counter()
        if os.path.exists(freq_path):
            with open(freq_path, 'r', encoding='utf-8') as f:
                keystrokes = json.load(f)
            keys = [k['key'].strip("'") for k in keystrokes if k['event'] == 'down' and k['key'].startswith("'") and len(k['key']) == 3]
            freq = Counter(keys)
        max_len = max(len(row) for row in layout)
        data = []
        label_grid = []
        for row in layout:
            row_data = [freq.get(k, 0) for k in row] + [0]*(max_len - len(row))
            row_labels = [k for k in row] + ['']*(max_len - len(row))
            data.append(row_data)
            label_grid.append(row_labels)
        
        self.ax2.clear()
        # Configurar colores para fondo oscuro
        plt.style.use('dark_background')
        im = self.ax2.imshow(data, cmap='YlGnBu', vmin=0)
        
        for i, row in enumerate(label_grid):
            for j, k in enumerate(row):
                if k:
                    freq_val = freq.get(k, 0)
                    max_freq = max(freq.values(), default=0)
                    if freq_val == max_freq and freq_val > 0:
                        color = '#FF6B6B'  # Rojo para teclas más frecuentes
                        font_weight = 'bold'
                    else:
                        color = 'white' if freq_val > 0 else '#AAAAAA'
                        font_weight = 'bold' if freq_val > 0 else 'normal'
                    self.ax2.text(j, i, k.upper(), ha='center', va='center', 
                                 color=color, fontsize=12, fontweight=font_weight)
        
        self.ax2.set_xticks([])
        self.ax2.set_yticks([])
        self.ax2.set_title('Layout optimizado (color: frecuencia de uso)\nPasa el mouse sobre las teclas para ver frecuencias', 
                          color='white', fontsize=12, fontweight='bold')
        
        # Configurar fondo transparente
        self.figure.patch.set_facecolor('none')
        self.ax2.set_facecolor('none')
        
        cbar = self.figure.colorbar(im, ax=self.ax2, orientation='vertical', fraction=0.025)
        cbar.ax.tick_params(colors='white')
        
        self.current_data = data
        self.current_labels = label_grid
        self.canvas.draw()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
