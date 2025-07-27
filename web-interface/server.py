#!/usr/bin/env python3
"""
Servidor backend para la interfaz web de KeySculptAI
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import sys
import os
import json
import threading
import time
from pathlib import Path

# Configurar el directorio raíz del proyecto
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

app = Flask(__name__)
CORS(app)

# Variables globales para el estado del sistema
system_status = {
    'keylogger': False,
    'analyzer': False,
    'optimizer': False,
    'remapper': False,
    'overlay': False
}

# Procesos activos
active_processes = {}

@app.route('/')
def serve_react_app():
    """Servir la aplicación React"""
    return send_from_directory('build', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Servir archivos estáticos"""
    return send_from_directory('build', path)

@app.route('/api/execute', methods=['POST'])
def execute_command():
    """Ejecutar comandos del sistema"""
    try:
        data = request.get_json()
        command = data.get('command')
        
        if not command:
            return jsonify({'error': 'Comando no especificado'}), 400
        
        # Mapear comandos a scripts
        command_map = {
            'keylogger': 'collector/keylogger.py',
            'analyzer': 'collector/analyzer.py',
            'optimizer': 'optimizer/genetic_optimizer.py',
            'ml_optimizer': 'optimizer/ml_optimizer.py',
            'remapper': 'remapper/windows_remap_simple.py',
            'overlay': 'overlay/realtime_overlay.py'
        }
        
        if command not in command_map:
            return jsonify({'error': f'Comando no válido: {command}'}), 400
        
        script_path = PROJECT_ROOT / command_map[command]
        
        if not script_path.exists():
            return jsonify({'error': f'Script no encontrado: {script_path}'}), 404
        
        # Ejecutar el comando
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
            timeout=30
        )
        
        # Actualizar estado del sistema
        if result.returncode == 0:
            if command == 'keylogger':
                system_status['keylogger'] = True
            elif command == 'analyzer':
                system_status['analyzer'] = True
            elif command == 'optimizer':
                system_status['optimizer'] = True
            elif command == 'remapper':
                system_status['remapper'] = True
            elif command == 'overlay':
                system_status['overlay'] = True
        
        return jsonify({
            'success': True,
            'command': command,
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Comando excedió el tiempo límite'}), 408
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/keystrokes', methods=['GET'])
def get_keystrokes():
    """Obtener datos de keystrokes"""
    try:
        keystrokes_file = PROJECT_ROOT / 'profiles' / 'keystrokes.json'
        
        # Si no hay datos reales, usar datos de demostración
        if not keystrokes_file.exists():
            demo_file = Path(__file__).parent / 'demo_data.json'
            if demo_file.exists():
                with open(demo_file, 'r', encoding='utf-8') as f:
                    return jsonify(json.load(f))
            else:
                return jsonify({'error': 'No hay datos de keystrokes disponibles'}), 404
        
        with open(keystrokes_file, 'r', encoding='utf-8') as f:
            keystrokes = json.load(f)
        
        # Procesar datos para el heatmap
        frequencies = {}
        for keystroke in keystrokes:
            if keystroke['event'] == 'down' and keystroke['key'].startswith("'") and len(keystroke['key']) == 3:
                key = keystroke['key'].strip("'")
                frequencies[key] = frequencies.get(key, 0) + 1
        
        return jsonify({
            'frequencies': frequencies,
            'total_keystrokes': len(keystrokes),
            'unique_keys': len(frequencies)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/layout', methods=['GET'])
def get_layout():
    """Obtener layout optimizado"""
    try:
        layout_file = PROJECT_ROOT / 'profiles' / 'best_layout.json'
        keystrokes_file = PROJECT_ROOT / 'profiles' / 'keystrokes.json'
        
        # Si no hay layout real, usar layout de demostración
        if not layout_file.exists():
            demo_file = Path(__file__).parent / 'demo_layout.json'
            if demo_file.exists():
                with open(demo_file, 'r', encoding='utf-8') as f:
                    return jsonify(json.load(f))
            else:
                return jsonify({'error': 'No hay layout optimizado disponible'}), 404
        
        with open(layout_file, 'r', encoding='utf-8') as f:
            layout = json.load(f)
        
        # Obtener frecuencias si están disponibles
        frequencies = {}
        if keystrokes_file.exists():
            with open(keystrokes_file, 'r', encoding='utf-8') as f:
                keystrokes = json.load(f)
            
            for keystroke in keystrokes:
                if keystroke['event'] == 'down' and keystroke['key'].startswith("'") and len(keystroke['key']) == 3:
                    key = keystroke['key'].strip("'")
                    frequencies[key] = frequencies.get(key, 0) + 1
        
        return jsonify({
            'layout': layout,
            'frequencies': frequencies,
            'improvement': 15.5  # Valor de ejemplo
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Obtener estado del sistema"""
    return jsonify(system_status)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Subir archivo"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No se proporcionó archivo'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No se seleccionó archivo'}), 400
        
        # Guardar archivo en el directorio de perfiles
        upload_dir = PROJECT_ROOT / 'profiles'
        upload_dir.mkdir(exist_ok=True)
        
        file_path = upload_dir / file.filename
        file.save(str(file_path))
        
        return jsonify({
            'success': True,
            'filename': file.filename,
            'path': str(file_path)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/processes', methods=['GET'])
def get_processes():
    """Obtener procesos activos"""
    return jsonify({
        'active_processes': list(active_processes.keys()),
        'count': len(active_processes)
    })

@app.route('/api/processes/<process_name>', methods=['DELETE'])
def stop_process(process_name):
    """Detener proceso específico"""
    try:
        if process_name in active_processes:
            process = active_processes[process_name]
            process.terminate()
            del active_processes[process_name]
            
            # Actualizar estado
            if process_name in system_status:
                system_status[process_name] = False
            
            return jsonify({'success': True, 'message': f'Proceso {process_name} detenido'})
        else:
            return jsonify({'error': f'Proceso {process_name} no encontrado'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Iniciando servidor backend de KeySculptAI...")
    print(f"📁 Directorio del proyecto: {PROJECT_ROOT}")
    print("🌐 Servidor disponible en: http://localhost:5000")
    
    # Crear directorio build si no existe (para desarrollo)
    build_dir = Path(__file__).parent / 'build'
    if not build_dir.exists():
        print("⚠️  Directorio 'build' no encontrado. Ejecuta 'npm run build' primero.")
        print("🔧 Para desarrollo, puedes usar 'npm start' en otra terminal.")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 