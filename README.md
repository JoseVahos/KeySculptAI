# 🎹 KeySculptAI - Optimizador de Teclado Inteligente

> [!NOTE]
> Este proyecto es una de mis primeras experiencias con el vibe coding. Se trata más de un experimento personal que de una herramienta real.

KeySculptAI es una herramienta avanzada que analiza tus patrones de escritura y optimiza la disposición de tu teclado para maximizar la eficiencia y reducir la fatiga.

## ✨ Características Principales

- **📊 Captura Inteligente**: Registra automáticamente tus patrones de escritura
- **🧠 Análisis Avanzado**: Procesa datos para identificar patrones de uso
- **⚡ Optimización Genética**: Algoritmos genéticos para encontrar el layout óptimo
- **🤖 Machine Learning**: Optimización basada en ML para resultados superiores
- **🎹 Remapeo en Tiempo Real**: Aplica layouts optimizados sin reiniciar
- **👁️ Overlay Visual**: Visualización en tiempo real de tu actividad
- **🌐 Interfaz Web Moderna**: Panel de control web con visualizaciones interactivas

## 🚀 Interfaz Web (Nueva!)

KeySculptAI ahora incluye una **interfaz web moderna** construida con HTML, CSS y JavaScript:

### 🌟 Características de la Interfaz Web

- **Diseño Glassmorphism**: Interfaz moderna con efectos de cristal
- **Visualizaciones Interactivas**: Heatmaps y layouts en tiempo real
- **Panel de Control Unificado**: Gestión completa desde el navegador
- **Logs en Tiempo Real**: Monitoreo detallado de todas las operaciones
- **Responsive Design**: Funciona en desktop, tablet y móvil
- **Notificaciones Toast**: Feedback visual inmediato
- **API RESTful**: Backend robusto con Flask

### 🎯 Componentes de la Interfaz

1. **Panel de Control**: Botones para todas las operaciones
2. **Heatmap Interactivo**: Visualización de frecuencias de teclas
3. **Comparador de Layouts**: QWERTY vs Optimizado lado a lado
4. **Sistema de Logs**: Registro completo con filtros
5. **Indicadores de Estado**: Estado en tiempo real de cada componente

## 📦 Instalación

### Prerrequisitos
- Python 3.8+
- Windows 10/11 (para el remapeo de teclas)
- Navegador web moderno

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/keysculpt-ai.git
cd keysculpt-ai
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Instalar dependencias de la interfaz web
```bash
cd web-interface
pip install flask flask-cors
```

## 🚀 Uso

### Opción 1: Interfaz Web (Recomendada)

#### Método 1: Scripts de Inicio (Más Fácil)
- **Windows**: Doble clic en `start_web_interface.bat`
- **PowerShell**: Ejecuta `.\start_web_interface.ps1`

#### Método 2: Línea de Comandos
1. **Iniciar el servidor backend**:
```bash
cd web-interface
python server.py
```

2. **Abrir en el navegador**: http://localhost:5000

3. **Usar la interfaz web**:
   - Haz clic en "🚀 Flujo Completo Automático" para ejecutar todo el pipeline
   - O usa los botones individuales para cada paso
   - Visualiza los resultados en las pestañas correspondientes

### Opción 2: Línea de Comandos

```bash
# 1. Capturar datos de escritura
python collector/keylogger.py

# 2. Analizar los datos capturados
python collector/analyzer.py

# 3. Optimizar el layout
python optimizer/genetic_optimizer.py

# 4. Aplicar el layout optimizado
python remapper/windows_remap_simple.py
```

### Opción 3: Interfaz PyQt5 (Legacy)

```bash
python overlay/overlay_ui.py
```

## 📁 Estructura del Proyecto

```
KeySculptAI/
├── collector/              # Captura y análisis de datos
│   ├── keylogger.py       # Registro de pulsaciones
│   └── analyzer.py        # Análisis de patrones
├── optimizer/             # Algoritmos de optimización
│   ├── genetic_optimizer.py
│   └── ml_optimizer.py
├── remapper/              # Remapeo de teclas
│   ├── windows_remap_v2.py
│   └── windows_remap_simple.py
├── overlay/               # Interfaz PyQt5
│   ├── overlay_ui.py
│   └── realtime_overlay.py
├── web-interface/         # 🌟 NUEVA Interfaz Web
│   ├── index.html         # Interfaz principal
│   ├── styles.css         # Estilos modernos
│   ├── script.js          # Funcionalidad JavaScript
│   ├── server.py          # Servidor Flask
│   └── README.md          # Documentación web
├── profiles/              # Datos y layouts guardados
│   ├── keystrokes.json
│   └── best_layout.json
└── requirements.txt       # Dependencias Python
```

## 🎨 Características de la Interfaz Web

### 🎛️ Panel de Control
- **Flujo Completo**: Ejecución automática de todo el pipeline
- **Captura de Datos**: Inicio del keylogger
- **Análisis**: Procesamiento de datos capturados
- **Optimización**: Generación de layout optimizado
- **Aplicación**: Activación del remapper
- **Overlay**: Visualización en tiempo real

### 📊 Visualizaciones
- **Heatmap Interactivo**: Frecuencias de teclas con colores
- **Comparador de Layouts**: QWERTY vs Optimizado
- **Estadísticas en Tiempo Real**: Métricas de uso y mejora
- **Tooltips Informativos**: Información detallada al hacer hover

### 📋 Sistema de Logs
- **Filtros por Tipo**: Info, Éxito, Advertencia, Error
- **Exportación**: Descarga de logs en formato texto
- **Copia al Portapapeles**: Funcionalidad de copia rápida
- **Scroll Automático**: Seguimiento de nuevos logs

### 🔔 Notificaciones
- **Toast Notifications**: Feedback visual inmediato
- **Auto-dismiss**: Desaparición automática después de 5 segundos
- **Diferentes Tipos**: Éxito, Error, Advertencia, Info
- **Cierre Manual**: Opción de cerrar manualmente

## 🔧 API Endpoints

La interfaz web se comunica con el backend a través de una API RESTful:

### Comandos del Sistema
- `POST /api/execute` - Ejecutar comandos (keylogger, analyzer, etc.)

### Datos
- `GET /api/keystrokes` - Obtener datos de pulsaciones
- `GET /api/layout` - Obtener layout optimizado
- `GET /api/status` - Estado del sistema

### Gestión de Archivos
- `POST /api/upload` - Subir archivos
- `GET /api/processes` - Procesos activos
- `DELETE /api/processes/<name>` - Detener proceso

## 🎯 Flujo de Trabajo

1. **📊 Captura**: Ejecutar keylogger para recopilar datos
2. **📈 Análisis**: Procesar datos para generar estadísticas
3. **⚡ Optimización**: Generar layout optimizado
4. **🎹 Aplicación**: Activar remapper con nuevo layout
5. **👁️ Monitoreo**: Usar overlay para visualización en tiempo real

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python**: Lógica principal y algoritmos
- **Flask**: Servidor web para la API
- **Flask-CORS**: Soporte para CORS
- **Subprocess**: Ejecución de scripts Python

### Frontend
- **HTML5**: Estructura semántica
- **CSS3**: Estilos modernos con glassmorphism
- **JavaScript ES6+**: Funcionalidad interactiva
- **Fetch API**: Comunicación con el backend

### Algoritmos
- **Algoritmos Genéticos**: Optimización de layouts
- **Machine Learning**: Análisis de patrones
- **Análisis de Frecuencias**: Estadísticas de uso

## 🐛 Solución de Problemas

### Error de CORS
Si encuentras errores de CORS:
- Verifica que el servidor Flask esté ejecutándose en el puerto 5000
- Asegúrate de que Flask-CORS esté instalado

### Error de Conexión
Si la aplicación no puede conectarse al backend:
- Verifica que el servidor Flask esté ejecutándose
- Revisa que no haya conflictos de puertos
- Asegúrate de acceder a http://localhost:5000

### Problemas con el Remapper
Si el remapper no funciona:
- Ejecuta como administrador
- Verifica que no haya otros programas usando el teclado
- Asegúrate de tener un layout optimizado generado

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Para soporte técnico o preguntas:
- Abre un issue en el repositorio
- Revisa la documentación en la carpeta `web-interface/`
- Contacta al equipo de desarrollo

## 🎉 Agradecimientos

- Comunidad de desarrolladores de Python
- Contribuidores de las librerías utilizadas
- Usuarios que han probado y mejorado el proyecto

---

**¡Optimiza tu experiencia de escritura con KeySculptAI!** 🚀

