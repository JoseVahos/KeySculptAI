#!/usr/bin/env python3
"""
Script de prueba para verificar que el remapper funcione correctamente
cuando se ejecuta como proceso hijo desde el overlay.
"""

import subprocess
import sys
import time
import os

def test_remapper_process():
    """Probar el remapper como proceso hijo"""
    print("🧪 [TEST] Probando remapper como proceso hijo...")
    
    # Ruta al remapper
    remapper_path = os.path.join('remapper', 'windows_remap_simple.py')
    
    if not os.path.exists(remapper_path):
        print(f"❌ [ERROR] No se encontró el archivo: {remapper_path}")
        return False
    
    try:
        # Configurar el proceso
        process = subprocess.Popen(
            [sys.executable, remapper_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,  # Line buffering
            universal_newlines=True
        )
        
        print(f"✅ [INFO] Proceso iniciado con PID: {process.pid}")
        
        # Leer la salida inicial
        output_lines = []
        start_time = time.time()
        
        while time.time() - start_time < 10:  # Esperar máximo 10 segundos
            if process.poll() is not None:
                # El proceso terminó
                break
                
            # Leer una línea de salida
            line = process.stdout.readline()
            if line:
                line = line.strip()
                output_lines.append(line)
                print(f"📤 [OUTPUT] {line}")
                
                # Si vemos que el remapper está activo, podemos terminar la prueba
                if "Remapeo activo" in line:
                    print("✅ [SUCCESS] Remapper iniciado correctamente!")
                    break
            else:
                time.sleep(0.1)
        
        # Terminar el proceso
        print("🛑 [INFO] Terminando proceso...")
        process.terminate()
        
        try:
            process.wait(timeout=5)
            print("✅ [SUCCESS] Proceso terminado correctamente")
        except subprocess.TimeoutExpired:
            print("⚠️ [WARNING] Proceso no terminó en 5 segundos, forzando...")
            process.kill()
            process.wait()
        
        # Mostrar resumen
        print(f"\n📊 [SUMMARY] Total de líneas de salida: {len(output_lines)}")
        print("📋 [OUTPUT] Primeras 10 líneas:")
        for i, line in enumerate(output_lines[:10]):
            print(f"  {i+1}: {line}")
        
        return True
        
    except Exception as e:
        print(f"❌ [ERROR] Error durante la prueba: {e}")
        return False

if __name__ == "__main__":
    success = test_remapper_process()
    if success:
        print("\n🎉 [SUCCESS] Prueba completada exitosamente!")
    else:
        print("\n💥 [FAILURE] La prueba falló!")
        sys.exit(1) 