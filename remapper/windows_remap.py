import json
import os
import sys
from pynput import keyboard
from pynput.keyboard import Key, KeyCode
import pyautogui
import threading
import time

class KeyboardRemapper:
    def __init__(self, layout_file=None):
        self.layout_file = layout_file or os.path.join(os.path.dirname(__file__), '..', 'profiles', 'best_layout.json')
        self.original_layout = self.load_qwerty_layout()
        self.optimized_layout = self.load_optimized_layout()
        self.remapping_active = False
        self.listener = None
        
        # Crear mapeo de teclas
        self.key_mapping = self.create_key_mapping()
        
    def load_qwerty_layout(self):
        """Cargar el layout QWERTY estándar"""
        return [
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm']
        ]
    
    def load_optimized_layout(self):
        """Cargar el layout optimizado desde el archivo JSON"""
        try:
            with open(self.layout_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ [ERROR] No se encontró el archivo de layout: {self.layout_file}")
            print("Ejecuta primero el optimizador para generar un layout.")
            return None
        except Exception as e:
            print(f"❌ [ERROR] Error al cargar el layout: {e}")
            return None
    
    def create_key_mapping(self):
        """Crear mapeo entre teclas originales y optimizadas"""
        if not self.optimized_layout:
            return {}
        
        mapping = {}
        original_flat = []
        optimized_flat = []
        
        # Aplanar ambos layouts
        for row in self.original_layout:
            original_flat.extend(row)
        
        for row in self.optimized_layout:
            optimized_flat.extend(row)
        
        # Crear mapeo
        for i, original_key in enumerate(original_flat):
            if i < len(optimized_flat):
                optimized_key = optimized_flat[i]
                mapping[original_key] = optimized_key
                mapping[optimized_key] = original_key  # Mapeo bidireccional
        
        return mapping
    
    def on_key_press(self, key):
        """Interceptar pulsaciones de teclas y remapearlas"""
        if not self.remapping_active:
            return True
        
        try:
            # Convertir la tecla a string
            if hasattr(key, 'char') and key.char:
                key_char = key.char.lower()
                
                # Verificar si necesitamos remapear
                if key_char in self.key_mapping:
                    # Bloquear la tecla original
                    return False
                    
            return True
        except AttributeError:
            return True
    
    def on_key_release(self, key):
        """Interceptar liberaciones de teclas y enviar la tecla remapeada"""
        if not self.remapping_active:
            return True
        
        try:
            if hasattr(key, 'char') and key.char:
                key_char = key.char.lower()
                
                # Verificar si necesitamos remapear
                if key_char in self.key_mapping:
                    # Enviar la tecla remapeada
                    remapped_key = self.key_mapping[key_char]
                    pyautogui.press(remapped_key)
                    return False
                    
            return True
        except AttributeError:
            return True
    
    def start_remapping(self):
        """Iniciar el remapeo de teclas"""
        if not self.key_mapping:
            print("❌ [ERROR] No hay mapeo de teclas disponible.")
            return False
        
        if self.remapping_active:
            print("⚠️ [INFO] El remapeo ya está activo.")
            return True
        
        print("🚀 [INFO] Iniciando remapeo de teclas...")
        print("📋 [INFO] Layout optimizado aplicado.")
        print("💡 [TIP] Presiona F12 para detener el remapeo.")
        
        self.remapping_active = True
        
        # Iniciar listener
        self.listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )
        self.listener.start()
        
        return True
    
    def stop_remapping(self):
        """Detener el remapeo de teclas"""
        if not self.remapping_active:
            print("⚠️ [INFO] El remapeo no está activo.")
            return True
        
        print("🛑 [INFO] Deteniendo remapeo de teclas...")
        print("📋 [INFO] Layout original restaurado.")
        
        self.remapping_active = False
        
        if self.listener:
            self.listener.stop()
            self.listener = None
        
        return True
    
    def get_layout_info(self):
        """Obtener información sobre el layout actual"""
        if not self.optimized_layout:
            return "No hay layout optimizado disponible."
        
        info = "📊 Layout Optimizado:\n"
        for i, row in enumerate(self.optimized_layout):
            info += f"Fila {i+1}: {' '.join(row).upper()}\n"
        
        info += f"\n🔄 Mapeos activos: {len(self.key_mapping)//2}"
        return info

def main():
    """Función principal para ejecutar el remapper"""
    print("🎹 KeySculptAI - Remapper de Teclado")
    print("=" * 50)
    
    remapper = KeyboardRemapper()
    
    if not remapper.optimized_layout:
        return
    
    print(remapper.get_layout_info())
    print("\n🎯 Controles:")
    print("- Presiona F12 para detener el remapeo")
    print("- Presiona ESC para salir")
    
    def on_control_key(key):
        try:
            if key == Key.f12:
                remapper.stop_remapping()
                return False
            elif key == Key.esc:
                remapper.stop_remapping()
                return False
        except AttributeError:
            pass
        return True
    
    # Listener para teclas de control
    control_listener = keyboard.Listener(on_press=on_control_key)
    control_listener.start()
    
    try:
        # Iniciar automáticamente
        if remapper.start_remapping():
            print("\n✅ Remapeo activo. Escribe normalmente para probar el layout optimizado.")
            print("💡 Las teclas se remapearán automáticamente según tu layout personalizado.")
            
            # Mantener activo hasta que se detenga
            while remapper.remapping_active:
                time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\n🛑 Interrumpido por el usuario.")
    finally:
        remapper.stop_remapping()
        control_listener.stop()
        print("👋 Remapper finalizado.")

if __name__ == "__main__":
    main()
