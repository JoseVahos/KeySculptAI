// Variables globales
let logs = [];
let currentFilter = 'all';
let isLoading = false;

// Configuración de la API
const API_BASE_URL = 'http://localhost:5000';

// Layout QWERTY estándar
const qwertyLayout = [
    ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
    ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
    ['z', 'x', 'c', 'v', 'b', 'n', 'm']
];

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    addLog('🚀 Aplicación KeySculptAI iniciada', 'info');
    renderKeyboardHeatmap();
    renderLayouts();
    updateLogFilters();
}

// Funciones de API
async function executeCommand(command, description) {
    if (isLoading) return;
    
    setLoading(true);
    addLog(`Iniciando: ${description}`, 'info');
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/execute`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ command })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            addLog(`✅ ${description} completado exitosamente`, 'success');
            showNotification(`${description} completado`, 'success');
            updateSystemStatus(command, true);
        } else {
            throw new Error(result.error || 'Error desconocido');
        }
        
    } catch (error) {
        addLog(`❌ Error en ${description}: ${error.message}`, 'error');
        showNotification(`Error en ${description}`, 'error');
    } finally {
        setLoading(false);
    }
}

async function runFullPipeline() {
    if (isLoading) return;
    
    setLoading(true);
    addLog('🚀 Iniciando flujo completo de optimización...', 'info');
    
    try {
        // Ejecutar en secuencia
        await executeCommand('keylogger', 'Captura de datos');
        await executeCommand('analyzer', 'Análisis de datos');
        await executeCommand('optimizer', 'Optimización de layout');
        
        showNotification('Flujo completo completado exitosamente', 'success');
    } catch (error) {
        addLog(`❌ Error en flujo completo: ${error.message}`, 'error');
        showNotification('Error en flujo completo', 'error');
    } finally {
        setLoading(false);
    }
}

async function getKeystrokesData() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/keystrokes`);
        if (response.ok) {
            return await response.json();
        } else {
            throw new Error('No se pudieron obtener los datos de keystrokes');
        }
    } catch (error) {
        console.error('Error obteniendo datos de keystrokes:', error);
        return null;
    }
}

async function getOptimizedLayout() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/layout`);
        if (response.ok) {
            return await response.json();
        } else {
            throw new Error('No se pudo obtener el layout optimizado');
        }
    } catch (error) {
        console.error('Error obteniendo layout optimizado:', error);
        return null;
    }
}

// Funciones de UI
function switchTab(tabName) {
    // Ocultar todas las pestañas
    document.querySelectorAll('.tab-pane').forEach(pane => {
        pane.classList.remove('active');
    });
    
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Mostrar la pestaña seleccionada
    document.getElementById(`${tabName}-tab`).classList.add('active');
    document.querySelector(`[onclick="switchTab('${tabName}')"]`).classList.add('active');
}

function setLoading(loading) {
    isLoading = loading;
    const overlay = document.getElementById('loading-overlay');
    
    if (loading) {
        overlay.classList.remove('hidden');
    } else {
        overlay.classList.add('hidden');
    }
}

function showNotification(message, type = 'info') {
    const container = document.getElementById('notification-container');
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    
    const icon = getNotificationIcon(type);
    notification.innerHTML = `
        <span>${icon}</span>
        <span>${message}</span>
        <span onclick="this.parentElement.remove()" style="cursor: pointer; margin-left: auto;">✕</span>
    `;
    
    container.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

function getNotificationIcon(type) {
    switch (type) {
        case 'success': return '✅';
        case 'error': return '❌';
        case 'warning': return '⚠️';
        default: return 'ℹ️';
    }
}

// Funciones de logs
function addLog(message, type = 'info') {
    const timestamp = new Date().toLocaleTimeString();
    const logEntry = { message, type, timestamp };
    logs.push(logEntry);
    
    updateLogDisplay();
    updateLogFilters();
}

function updateLogDisplay() {
    const container = document.getElementById('log-container');
    const filteredLogs = currentFilter === 'all' 
        ? logs 
        : logs.filter(log => log.type === currentFilter);
    
    if (filteredLogs.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>No hay logs para mostrar</p></div>';
        return;
    }
    
    container.innerHTML = filteredLogs.map(log => `
        <div class="log-entry ${log.type}">
            <span class="log-timestamp">${log.timestamp}</span>
            <span class="log-message ${log.type}">${log.message}</span>
        </div>
    `).join('');
    
    // Scroll to bottom
    container.scrollTop = container.scrollHeight;
}

function updateLogFilters() {
    const logTypes = [
        { key: 'all', label: 'Todos' },
        { key: 'info', label: 'Info' },
        { key: 'success', label: 'Éxito' },
        { key: 'warning', label: 'Advertencia' },
        { key: 'error', label: 'Error' }
    ];
    
    const filterContainer = document.querySelector('.log-filters');
    filterContainer.innerHTML = logTypes.map(({ key, label }) => {
        const count = key === 'all' ? logs.length : logs.filter(log => log.type === key).length;
        const activeClass = currentFilter === key ? 'active' : '';
        return `<button class="filter-btn ${activeClass}" onclick="filterLogs('${key}')">${label} (${count})</button>`;
    }).join('');
}

function filterLogs(filter) {
    currentFilter = filter;
    updateLogDisplay();
    updateLogFilters();
}

function clearLogs() {
    logs = [];
    updateLogDisplay();
    updateLogFilters();
}

function downloadLogs() {
    const logText = logs.map(log => 
        `[${log.timestamp}] ${log.type.toUpperCase()}: ${log.message}`
    ).join('\n');
    
    const blob = new Blob([logText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `keysculpt-logs-${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Funciones de visualización
async function renderKeyboardHeatmap() {
    const container = document.getElementById('keyboard-heatmap');
    const data = await getKeystrokesData();
    
    if (!data || !data.frequencies) {
        container.innerHTML = '<div class="empty-state"><p>No hay datos disponibles. Ejecuta el keylogger para capturar datos.</p></div>';
        return;
    }
    
    const maxFreq = Math.max(...Object.values(data.frequencies));
    
    container.innerHTML = qwertyLayout.map((row, rowIndex) => 
        row.map((key, colIndex) => {
            const frequency = data.frequencies[key] || 0;
            const intensity = maxFreq > 0 ? frequency / maxFreq : 0;
            const alpha = 0.1 + (intensity * 0.9);
            
            return `
                <div class="key" 
                     style="grid-column: ${rowIndex === 1 ? colIndex + 2 : rowIndex === 2 ? colIndex + 3 : colIndex + 1}; 
                            background: rgba(255, 107, 107, ${alpha});"
                     title="${key.toUpperCase()}: ${frequency} pulsaciones">
                    ${key.toUpperCase()}
                </div>
            `;
        }).join('')
    ).join('');
    
    // Actualizar estadísticas
    updateHeatmapStats(data);
}

function updateHeatmapStats(data) {
    const totalKeystrokes = Object.values(data.frequencies).reduce((sum, freq) => sum + freq, 0);
    const uniqueKeys = Object.keys(data.frequencies).length;
    const maxFrequency = Math.max(...Object.values(data.frequencies));
    const mostUsedKey = Object.entries(data.frequencies).reduce((a, b) => 
        data.frequencies[a[0]] > data.frequencies[b[0]] ? a : b
    )[0].toUpperCase();
    
    document.getElementById('total-keystrokes').textContent = totalKeystrokes;
    document.getElementById('most-used-key').textContent = mostUsedKey;
    document.getElementById('unique-keys').textContent = uniqueKeys;
    document.getElementById('max-frequency').textContent = Math.round(maxFrequency);
}

async function renderLayouts() {
    const qwertyContainer = document.getElementById('qwerty-layout');
    const optimizedContainer = document.getElementById('optimized-layout');
    const data = await getOptimizedLayout();
    
    // Renderizar QWERTY
    qwertyContainer.innerHTML = qwertyLayout.map(row => `
        <div class="keyboard-row">
            ${row.map(key => `
                <div class="layout-key" title="${key.toUpperCase()}">
                    ${key.toUpperCase()}
                </div>
            `).join('')}
        </div>
    `).join('');
    
    // Renderizar optimizado
    if (data && data.layout) {
        optimizedContainer.innerHTML = data.layout.map(row => `
            <div class="keyboard-row">
                ${row.map(key => `
                    <div class="layout-key optimized" title="${key.toUpperCase()}">
                        ${key.toUpperCase()}
                    </div>
                `).join('')}
            </div>
        `).join('');
        
        updateLayoutStats(data);
    } else {
        optimizedContainer.innerHTML = '<div class="empty-state"><p>No hay layout optimizado disponible. Ejecuta el optimizador primero.</p></div>';
    }
}

function updateLayoutStats(data) {
    const optimizedKeys = data.layout ? data.layout.flat().length : 0;
    const improvement = data.improvement || 0;
    const efficiency = Math.round((optimizedKeys / 26) * 100);
    
    document.getElementById('optimized-keys').textContent = optimizedKeys;
    document.getElementById('improvement').textContent = `${Math.round(improvement * 100) / 100}%`;
    document.getElementById('efficiency').textContent = `${efficiency}%`;
}

function updateSystemStatus(command, active) {
    const statusMap = {
        'keylogger': 'keylogger-status',
        'analyzer': 'analyzer-status',
        'optimizer': 'optimizer-status',
        'remapper': 'remapper-status'
    };
    
    const statusElement = document.getElementById(statusMap[command]);
    if (statusElement) {
        statusElement.textContent = active ? '✅ Activo' : '❌ Inactivo';
    }
}

// Funciones de actualización
function refreshHeatmap() {
    renderKeyboardHeatmap();
    showNotification('Heatmap actualizado', 'info');
}

function refreshLayout() {
    renderLayouts();
    showNotification('Layout actualizado', 'info');
}

// Manejo de errores global
window.addEventListener('error', function(event) {
    addLog(`Error de JavaScript: ${event.error.message}`, 'error');
});

// Manejo de errores de red
window.addEventListener('unhandledrejection', function(event) {
    addLog(`Error de red: ${event.reason}`, 'error');
}); 