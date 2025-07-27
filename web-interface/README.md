# KeySculptAI - Interfaz Web

Interfaz web moderna para KeySculptAI construida con React, TypeScript y Flask.

## 🚀 Características

- **Interfaz moderna**: Diseño responsive con glassmorphism y animaciones suaves
- **Visualizaciones interactivas**: Heatmaps y layouts optimizados en tiempo real
- **Panel de control**: Gestión completa de todos los componentes del sistema
- **Logs en tiempo real**: Monitoreo detallado de todas las operaciones
- **API RESTful**: Backend robusto con Flask para comunicación con Python

## 🛠️ Tecnologías

### Frontend
- **React 18**: Biblioteca de interfaz de usuario
- **Styled Components**: CSS-in-JS para estilos
- **Framer Motion**: Animaciones fluidas
- **Lucide React**: Iconos modernos
- **Axios**: Cliente HTTP

### Backend
- **Flask**: Framework web para Python
- **Flask-CORS**: Soporte para CORS
- **Subprocess**: Ejecución de scripts Python

## 📦 Instalación

### Prerrequisitos
- Node.js 16+ y npm
- Python 3.8+
- Todas las dependencias de KeySculptAI instaladas

### 1. Instalar dependencias del frontend
```bash
cd web-interface
npm install
```

### 2. Instalar dependencias del backend
```bash
pip install flask flask-cors
```

## 🚀 Desarrollo

### Opción 1: Desarrollo con servidor separado (Recomendado)

1. **Iniciar el servidor backend**:
```bash
cd web-interface
python server.py
```

2. **Iniciar el servidor de desarrollo de React** (en otra terminal):
```bash
cd web-interface
npm start
```

3. **Acceder a la aplicación**:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

### Opción 2: Desarrollo integrado

1. **Construir la aplicación React**:
```bash
cd web-interface
npm run build
```

2. **Iniciar solo el servidor Flask**:
```bash
cd web-interface
python server.py
```

3. **Acceder a la aplicación**: http://localhost:5000

## 📁 Estructura del Proyecto

```
web-interface/
├── public/                 # Archivos públicos
│   └── index.html         # HTML principal
├── src/                   # Código fuente React
│   ├── components/        # Componentes React
│   │   ├── KeyboardHeatmap.js
│   │   ├── OptimizedLayout.js
│   │   └── LogViewer.js
│   ├── services/          # Servicios de API
│   │   └── api.js
│   ├── App.js            # Componente principal
│   ├── index.js          # Punto de entrada
│   └── index.css         # Estilos globales
├── server.py             # Servidor Flask
├── package.json          # Dependencias Node.js
└── README.md            # Esta documentación
```

## 🔧 API Endpoints

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

## 🎨 Componentes Principales

### KeyboardHeatmap
Visualización interactiva de las frecuencias de pulsación de teclas con:
- Heatmap colorido del teclado QWERTY
- Tooltips con información detallada
- Estadísticas en tiempo real
- Animaciones suaves

### OptimizedLayout
Comparación lado a lado de layouts:
- Layout QWERTY original
- Layout optimizado generado
- Estadísticas de mejora
- Visualización de frecuencias

### LogViewer
Sistema de logs avanzado con:
- Filtros por tipo de log
- Exportación de logs
- Copia al portapapeles
- Scroll automático

## 🎯 Funcionalidades

### Panel de Control
- **Flujo Completo**: Ejecución automática de todo el pipeline
- **Captura de Datos**: Inicio del keylogger
- **Análisis**: Procesamiento de datos capturados
- **Optimización**: Generación de layout optimizado
- **Aplicación**: Activación del remapper
- **Overlay**: Visualización en tiempo real

### Estado del Sistema
- Indicadores visuales del estado de cada componente
- Actualización en tiempo real
- Notificaciones de éxito/error

### Notificaciones
- Sistema de notificaciones toast
- Diferentes tipos: éxito, error, advertencia, info
- Auto-dismiss con opción de cerrar manualmente

## 🔄 Flujo de Trabajo

1. **Captura**: Ejecutar keylogger para recopilar datos
2. **Análisis**: Procesar datos para generar estadísticas
3. **Optimización**: Generar layout optimizado
4. **Aplicación**: Activar remapper con nuevo layout
5. **Monitoreo**: Usar overlay para visualización en tiempo real

## 🐛 Solución de Problemas

### Error de CORS
Si encuentras errores de CORS, asegúrate de que:
- El servidor Flask esté ejecutándose en el puerto 5000
- Flask-CORS esté instalado y configurado

### Error de Conexión
Si la aplicación no puede conectarse al backend:
- Verifica que el servidor Flask esté ejecutándose
- Revisa la configuración del proxy en package.json
- Asegúrate de que no haya conflictos de puertos

### Problemas de Construcción
Si hay problemas al construir la aplicación:
```bash
npm run build
```
- Verifica que todas las dependencias estén instaladas
- Revisa la consola para errores específicos

## 📝 Scripts Disponibles

- `npm start` - Iniciar servidor de desarrollo
- `npm run build` - Construir para producción
- `npm test` - Ejecutar tests
- `npm run eject` - Eyectar configuración (irreversible)

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la misma licencia que KeySculptAI.

## 🆘 Soporte

Para soporte técnico o preguntas:
- Revisa la documentación principal de KeySculptAI
- Abre un issue en el repositorio
- Contacta al equipo de desarrollo 