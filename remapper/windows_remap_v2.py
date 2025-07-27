import json
import os
import sys
import keyboard
import time
import threading
from collections import defaultdict

# Configurar codificación UTF-8 para evitar problemas con emojis
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

class ImprovedKeyboardRemapper:
    def __init__(self, layout_file=None):
        self.layout_file = layout_file or os.path.join(os.path.dirname(__file__), '..', 'profiles', 'best_layout.json')
        self.original_layout = self.load_qwerty_layout()
        self.optimized_layout = self.load_optimized_layout()
        self.remapping_active = False
        self.key_mapping = {}
        self.reverse_mapping = {}
        
        if self.optimized_layout:
            self.create_key_mapping()
        
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
            return
        
        # Aplanar ambos layouts
        original_flat = []
        optimized_flat = []
        
        for row in self.original_layout:
            original_flat.extend(row)
        
        for row in self.optimized_layout:
            optimized_flat.extend(row)
        
        # Crear mapeo unidireccional (QWERTY -> Optimizado)
        self.key_mapping = {}
        self.reverse_mapping = {}
        
        print(f"🔍 [DEBUG] Layout original: {original_flat}")
        print(f"🔍 [DEBUG] Layout optimizado: {optimized_flat}")
        
        for i, original_key in enumerate(original_flat):
            if i < len(optimized_flat):
                optimized_key = optimized_flat[i]
                if original_key != optimized_key:  # Solo mapear si son diferentes
                    self.key_mapping[original_key] = optimized_key
                    self.reverse_mapping[optimized_key] = original_key
                    print(f"🔍 [DEBUG] Mapeo: '{original_key}' → '{optimized_key}'")
        
        print(f"✅ [INFO] Mapeo creado: {len(self.key_mapping)} teclas diferentes")
        
        if not self.key_mapping:
            print("⚠️ [WARNING] No hay diferencias entre layouts. El remapeo no tendrá efecto.")
    
    def on_key_event(self, event):
        """Manejar eventos de teclas"""
        if not self.remapping_active:
            return
        
        try:
            # Solo procesar pulsaciones de teclas
            if event.event_type == keyboard.KEY_DOWN:
                key = event.name.lower()
                
                # Verificar si necesitamos remapear
                if key in self.key_mapping:
                    print(f"🔄 [REMAP] '{key}' → '{self.key_mapping[key]}'")
                    # Bloquear la tecla original
                    return False
                    
        except Exception as e:
            print(f"⚠️ [WARNING] Error procesando tecla: {e}")
        
        return True
    
    def send_remapped_key(self, original_key):
        """Enviar la tecla remapeada"""
        if original_key in self.key_mapping:
            remapped_key = self.key_mapping[original_key]
            try:
                # Simular la pulsación de la tecla remapeada
                keyboard.press_and_release(remapped_key)
                return True
            except Exception as e:
                print(f"⚠️ [WARNING] Error enviando tecla remapeada: {e}")
                return False
        return False
    
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
        
        # Registrar hooks para todas las teclas mapeadas
        for original_key in self.key_mapping.keys():
            keyboard.on_press_key(original_key, self.on_key_event, suppress=True)
            # También registrar el evento de liberación para enviar la tecla remapeada
            keyboard.on_release_key(original_key, lambda e, key=original_key: self.send_remapped_key(key), suppress=True)
        
        return True
    
    def stop_remapping(self):
        """Detener el remapeo de teclas"""
        if not self.remapping_active:
            print("⚠️ [INFO] El remapeo no está activo.")
            return True
        
        print("🛑 [INFO] Deteniendo remapeo de teclas...")
        print("📋 [INFO] Layout original restaurado.")
        
        self.remapping_active = False
        
        # Limpiar todos los hooks
        keyboard.unhook_all()
        
        return True
    
    def get_layout_info(self):
        """Obtener información sobre el layout actual"""
        if not self.optimized_layout:
            return "No hay layout optimizado disponible."
        
        info = "📊 Layout Optimizado:\n"
        for i, row in enumerate(self.optimized_layout):
            info += f"Fila {i+1}: {' '.join(row).upper()}\n"
        
        info += f"\n🔄 Mapeos activos: {len(self.key_mapping)}"
        
        # Mostrar algunos ejemplos de mapeo
        info += "\n\n📝 Ejemplos de mapeo:"
        examples = list(self.key_mapping.items())[:5]
        for original, remapped in examples:
            info += f"\n  '{original}' → '{remapped}'"
        
        return info
    
    def test_mapping(self):
        """Probar el mapeo actual de forma interactiva"""
        print("\n🧪 [TEST] Modo de prueba activado")
        print("📝 Escribe cualquier letra para ver cómo se remapea:")
        print("💡 Las teclas se mostrarán como: 'tecla_presionada' → 'tecla_remapeada'")
        print("🛑 Presiona F12 para salir del modo de prueba")
        
        self.test_mode = True
        
        def on_test_key(event):
            if event.event_type == keyboard.KEY_DOWN and self.test_mode:
                key = event.name.lower()
                if key in self.key_mapping:
                    print(f"  🎯 '{key}' → '{self.key_mapping[key]}'")
                else:
                    print(f"  ⚪ '{key}' → '{key}' (sin cambios)")
        
        # Registrar hook temporal para testing
        keyboard.hook(on_test_key)
        
        # Esperar hasta F12
        keyboard.wait('f12')
        keyboard.unhook_all()
        self.test_mode = False
        print("✅ [TEST] Modo de prueba finalizado")
    
    def show_mapping_summary(self):
        """Mostrar un resumen completo del mapeo"""
        print("\n📊 RESUMEN DEL MAPEO:")
        print("=" * 40)
        
        if not self.key_mapping:
            print("❌ No hay mapeos activos")
            return
        
        # Agrupar por filas para mejor visualización
        qwerty_rows = [
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm']
        ]
        
        print("🎹 Layout QWERTY → Layout Optimizado:")
        print()
        
        for row_idx, row in enumerate(qwerty_rows):
            print(f"Fila {row_idx + 1}: ", end="")
            for key in row:
                if key in self.key_mapping:
                    print(f"[{key}→{self.key_mapping[key]}] ", end="")
                else:
                    print(f"[{key}] ", end="")
            print()
        
        print(f"\n📈 Estadísticas:")
        print(f"  • Teclas remapeadas: {len(self.key_mapping)}")
        print(f"  • Teclas sin cambios: {26 - len(self.key_mapping)}")
        print(f"  • Porcentaje de cambio: {(len(self.key_mapping)/26)*100:.1f}%")
        
        # Mostrar las teclas más importantes (más frecuentes)
        print(f"\n🎯 Teclas más importantes remapeadas:")
        important_keys = ['e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'l']
        for key in important_keys:
            if key in self.key_mapping:
                print(f"  • '{key}' → '{self.key_mapping[key]}'")

def main():
    """Función principal para ejecutar el remapper"""
    # Configurar codificación UTF-8 para la salida
    if sys.platform == "win32":
        import codecs
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
        sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())
    
    print("KeySculptAI - Remapper Mejorado de Teclado")
    print("=" * 60)
    
    remapper = ImprovedKeyboardRemapper()
    
    if not remapper.optimized_layout:
        print("ERROR: No se pudo cargar el layout optimizado.")
        return 1
    
    print(remapper.get_layout_info())
    remapper.show_mapping_summary()
    print("\nControles:")
    print("- Presiona F12 para detener el remapeo")
    print("- Presiona ESC para salir")
    print("- Presiona T para probar el mapeo interactivamente")
    print("- Presiona S para mostrar resumen del mapeo")
    
    def on_control_key(event):
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'f12':
                print("\nINFO: Deteniendo remapeo por F12...")
                remapper.stop_remapping()
                return False
            elif event.name == 'esc':
                print("\nINFO: Deteniendo remapeo por ESC...")
                remapper.stop_remapping()
                return False
            elif event.name == 't':
                remapper.test_mapping()
                return False
            elif event.name == 's':
                remapper.show_mapping_summary()
                return False
        return True
    
    # Registrar teclas de control
    keyboard.on_press_key('f12', on_control_key)
    keyboard.on_press_key('esc', on_control_key)
    keyboard.on_press_key('t', on_control_key)
    keyboard.on_press_key('s', on_control_key)
    
    try:
        # Iniciar automáticamente
        if remapper.start_remapping():
            print("\nSUCCESS: Remapeo activo. Escribe normalmente para probar el layout optimizado.")
            print("TIP: Las teclas se remapearán automáticamente según tu layout personalizado.")
            print("CONTROLS: Presiona 'T' para probar el mapeo, F12 para detener.")
            
            # Mantener activo hasta que se detenga
            while remapper.remapping_active:
                time.sleep(0.1)
                
            print("SUCCESS: Remapeo detenido correctamente.")
            return 0
        else:
            print("ERROR: No se pudo iniciar el remapeo.")
            return 1
    
    except KeyboardInterrupt:
        print("\nINFO: Interrumpido por el usuario.")
        return 0
    except Exception as e:
        print(f"\nERROR: Error inesperado: {e}")
        return 1
    finally:
        try:
            remapper.stop_remapping()
            keyboard.unhook_all()
            print("INFO: Remapper finalizado.")
        except:
            pass  # Ignorar errores en la limpieza

if __name__ == "__main__":
    main() 