# 🎹 Cómo Usar KeySculptAI

## 🚀 Inicio Rápido

### Paso 1: Iniciar la Interfaz Web
**Opción A: Script Automático (Recomendado)**
- Doble clic en `start_web_interface.bat`
- Se abrirá automáticamente el servidor

**Opción B: Manual**
```bash
cd web-interface
python server.py
```

### Paso 2: Abrir en el Navegador
- Ve a: http://localhost:5000
- ¡Ya puedes usar la interfaz!

## 🎯 Guía de Uso Completa

### 1. Panel de Control Principal

#### 🚀 Flujo Completo Automático
- **¿Qué hace?**: Ejecuta todo el proceso automáticamente
- **Cuándo usar**: Primera vez o cuando quieras optimizar desde cero
- **Proceso**: Captura → Analiza → Optimiza → Aplica

#### 📊 Capturar Datos
- **¿Qué hace?**: Inicia el keylogger para registrar tus pulsaciones
- **Cuándo usar**: Cuando quieras recopilar nuevos datos
- **Duración**: Recomendado 10-30 minutos de escritura normal

#### 📈 Analizar Datos
- **¿Qué hace?**: Procesa los datos capturados para generar estadísticas
- **Cuándo usar**: Después de capturar datos
- **Resultado**: Heatmap y estadísticas de uso

#### ⚡ Optimizar Layout
- **¿Qué hace?**: Genera un layout optimizado usando algoritmos genéticos
- **Cuándo usar**: Después del análisis
- **Resultado**: Layout personalizado para tu patrón de escritura

#### 🎹 Aplicar Layout
- **¿Qué hace?**: Activa el remapper con el layout optimizado
- **Cuándo usar**: Cuando tengas un layout optimizado
- **Nota**: Requiere permisos de administrador

#### 👁️ Lanzar Overlay
- **¿Qué hace?**: Muestra visualización en tiempo real
- **Cuándo usar**: Para monitorear tu actividad actual

### 2. Pestañas de Visualización

#### 📊 Heatmap
- **Visualización**: Teclado con colores según frecuencia de uso
- **Información**: Hover sobre teclas para ver estadísticas
- **Estadísticas**: Total de pulsaciones, tecla más usada, etc.

#### ⚡ Layout Optimizado
- **Comparación**: QWERTY original vs Layout optimizado
- **Colores**: Verde para teclas optimizadas
- **Métricas**: Mejora de eficiencia, teclas optimizadas

#### 📋 Logs
- **Registro**: Todas las operaciones del sistema
- **Filtros**: Por tipo (Info, Éxito, Advertencia, Error)
- **Acciones**: Copiar, descargar, limpiar logs

### 3. Indicadores de Estado

- **📊 Keylogger**: Activo/Inactivo
- **📈 Analizador**: Completado/Pendiente
- **⚡ Optimizador**: Completado/Pendiente
- **🎹 Remapper**: Activo/Inactivo

## 🔄 Flujo de Trabajo Típico

### Primera Vez
1. **Iniciar** la interfaz web
2. **Capturar datos** (escribir normalmente por 15-30 minutos)
3. **Analizar** los datos capturados
4. **Optimizar** el layout
5. **Aplicar** el layout optimizado
6. **Probar** el nuevo layout

### Uso Regular
1. **Aplicar layout** (si ya tienes uno optimizado)
2. **Lanzar overlay** para monitorear
3. **Capturar nuevos datos** periódicamente para mejorar

## 🎨 Características de la Interfaz

### Diseño Moderno
- **Glassmorphism**: Efectos de cristal y transparencias
- **Responsive**: Funciona en desktop, tablet y móvil
- **Animaciones**: Transiciones suaves y efectos hover

### Feedback Visual
- **Notificaciones toast**: Mensajes de éxito/error
- **Indicadores de carga**: Spinner durante operaciones
- **Estados visuales**: Botones cambian según el estado

### Interactividad
- **Tooltips**: Información detallada al hacer hover
- **Filtros**: En logs y visualizaciones
- **Controles**: Botones de actualizar y exportar

## 🔧 Configuración Avanzada

### Modo de Demostración
Si no tienes datos reales, la interfaz mostrará datos de demostración para que puedas ver cómo funciona.

### Personalización
- **Colores**: Modifica `styles.css` para cambiar el tema
- **Funcionalidad**: Edita `script.js` para agregar características
- **Backend**: Modifica `server.py` para cambiar la lógica

## 🐛 Solución de Problemas

### El servidor no inicia
```bash
# Verificar Python
python --version

# Instalar dependencias
pip install flask flask-cors
```

### Error de conexión
- Verifica que el puerto 5000 esté libre
- Reinicia el servidor
- Revisa los logs del navegador (F12)

### El remapper no funciona
- Ejecuta como administrador
- Verifica que no haya otros programas usando el teclado
- Asegúrate de tener un layout optimizado

### Interfaz no se carga
- Verifica que el servidor esté ejecutándose
- Limpia la caché del navegador
- Prueba en modo incógnito

## 📊 Interpretación de Resultados

### Heatmap
- **Rojo intenso**: Teclas muy usadas
- **Rojo claro**: Teclas moderadamente usadas
- **Transparente**: Teclas poco usadas

### Layout Optimizado
- **Verde**: Teclas optimizadas
- **Mejora de eficiencia**: Porcentaje de mejora esperada
- **Teclas optimizadas**: Número de teclas reubicadas

### Estadísticas
- **Total de pulsaciones**: Volumen total de escritura
- **Tecla más usada**: Tu tecla más frecuente
- **Teclas únicas**: Diversidad de tu escritura

## 🎯 Consejos de Uso

### Para Mejores Resultados
1. **Escribe naturalmente**: No cambies tu forma de escribir durante la captura
2. **Usa diferentes tipos de texto**: Código, documentos, emails, etc.
3. **Captura suficiente datos**: Mínimo 15 minutos, ideal 30+ minutos
4. **Prueba el layout**: Usa el layout optimizado por varios días
5. **Itera**: Captura nuevos datos y reoptimiza periódicamente

### Optimización Continua
- **Captura semanal**: Para mantener el layout actualizado
- **Diferentes contextos**: Trabajo, ocio, diferentes idiomas
- **Ajustes manuales**: Puedes modificar el layout si es necesario

## 🆘 Soporte

### Recursos Disponibles
- **README.md**: Documentación completa del proyecto
- **INSTRUCCIONES_RAPIDAS.md**: Guía de inicio rápido
- **Logs**: Información detallada de errores
- **Issues**: Reportar problemas en el repositorio

### Comunidad
- **GitHub**: Reportar bugs y solicitar características
- **Discord/Slack**: Comunidad de usuarios (si está disponible)
- **Documentación**: Wiki del proyecto

---

**¡Disfruta optimizando tu experiencia de escritura!** 🚀✨ 