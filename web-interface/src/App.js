import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Play, 
  BarChart3, 
  Zap, 
  Brain, 
  Eye, 
  Keyboard, 
  Settings, 
  Download,
  Upload,
  Activity,
  CheckCircle,
  AlertCircle,
  X
} from 'lucide-react';
import KeyboardHeatmap from './components/KeyboardHeatmap';
import OptimizedLayout from './components/OptimizedLayout';
import LogViewer from './components/LogViewer';
import { executeCommand } from './services/api';

const AppContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  font-family: 'Inter', sans-serif;
`;

const Header = styled(motion.header)`
  text-align: center;
  margin-bottom: 40px;
  color: white;
`;

const Title = styled.h1`
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 10px;
  background: linear-gradient(45deg, #fff, #f0f0f0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
`;

const Subtitle = styled.p`
  font-size: 1.2rem;
  opacity: 0.9;
  font-weight: 300;
`;

const MainContent = styled.div`
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 30px;
  
  @media (max-width: 1200px) {
    grid-template-columns: 1fr;
  }
`;

const ControlPanel = styled(motion.div)`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 30px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  height: fit-content;
`;

const ActionButton = styled(motion.button)`
  width: 100%;
  padding: 15px 20px;
  margin-bottom: 15px;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  transition: all 0.3s ease;
  background: ${props => props.variant === 'primary' ? 'linear-gradient(45deg, #667eea, #764ba2)' : 
                props.variant === 'success' ? 'linear-gradient(45deg, #4ade80, #22c55e)' :
                props.variant === 'warning' ? 'linear-gradient(45deg, #f59e0b, #d97706)' :
                props.variant === 'danger' ? 'linear-gradient(45deg, #ef4444, #dc2626)' :
                'rgba(255, 255, 255, 0.1)'};
  color: white;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
`;

const StatusIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  margin-bottom: 20px;
  font-weight: 500;
`;

const VisualizationPanel = styled(motion.div)`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 30px;
  border: 1px solid rgba(255, 255, 255, 0.2);
`;

const TabContainer = styled.div`
  display: flex;
  margin-bottom: 20px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  padding: 5px;
`;

const Tab = styled.button`
  flex: 1;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  background: ${props => props.active ? 'rgba(255, 255, 255, 0.2)' : 'transparent'};
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(255, 255, 255, 0.1);
  }
`;

const Notification = styled(motion.div)`
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 15px 20px;
  border-radius: 10px;
  color: white;
  font-weight: 500;
  z-index: 1000;
  background: ${props => props.type === 'success' ? '#10b981' : 
                props.type === 'error' ? '#ef4444' : 
                props.type === 'warning' ? '#f59e0b' : '#3b82f6'};
  display: flex;
  align-items: center;
  gap: 10px;
  max-width: 400px;
`;

function App() {
  const [activeTab, setActiveTab] = useState('heatmap');
  const [logs, setLogs] = useState([]);
  const [status, setStatus] = useState({
    keylogger: false,
    analyzer: false,
    optimizer: false,
    remapper: false,
    overlay: false
  });
  const [notification, setNotification] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const showNotification = (message, type = 'info') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 5000);
  };

  const addLog = (message, type = 'info') => {
    const timestamp = new Date().toLocaleTimeString();
    setLogs(prev => [...prev, { message, type, timestamp }]);
  };

  const handleCommand = async (command, description) => {
    setIsLoading(true);
    addLog(`Iniciando: ${description}`, 'info');
    
    try {
      const result = await executeCommand(command);
      addLog(`✅ ${description} completado exitosamente`, 'success');
      showNotification(`${description} completado`, 'success');
      
      // Actualizar estado según el comando
      if (command === 'keylogger') {
        setStatus(prev => ({ ...prev, keylogger: true }));
      } else if (command === 'analyzer') {
        setStatus(prev => ({ ...prev, analyzer: true }));
      } else if (command === 'optimizer') {
        setStatus(prev => ({ ...prev, optimizer: true }));
      } else if (command === 'remapper') {
        setStatus(prev => ({ ...prev, remapper: true }));
      }
      
    } catch (error) {
      addLog(`❌ Error en ${description}: ${error.message}`, 'error');
      showNotification(`Error en ${description}`, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const runFullPipeline = async () => {
    setIsLoading(true);
    addLog('🚀 Iniciando flujo completo de optimización...', 'info');
    
    try {
      // Ejecutar en secuencia
      await handleCommand('keylogger', 'Captura de datos');
      await handleCommand('analyzer', 'Análisis de datos');
      await handleCommand('optimizer', 'Optimización de layout');
      
      showNotification('Flujo completo completado exitosamente', 'success');
    } catch (error) {
      addLog(`❌ Error en flujo completo: ${error.message}`, 'error');
      showNotification('Error en flujo completo', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AppContainer>
      <Header
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <Title>🎹 KeySculptAI</Title>
        <Subtitle>Optimizador de Teclado Inteligente</Subtitle>
      </Header>

      <MainContent>
        <ControlPanel
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          <h2 style={{ color: 'white', marginBottom: '20px', fontSize: '1.5rem' }}>
            Panel de Control
          </h2>

          <ActionButton
            variant="primary"
            onClick={runFullPipeline}
            disabled={isLoading}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <Play size={20} />
            Flujo Completo Automático
          </ActionButton>

          <ActionButton
            onClick={() => handleCommand('keylogger', 'Captura de datos')}
            disabled={isLoading}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <Activity size={20} />
            Capturar Datos
          </ActionButton>

          <ActionButton
            onClick={() => handleCommand('analyzer', 'Análisis de datos')}
            disabled={isLoading}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <BarChart3 size={20} />
            Analizar Datos
          </ActionButton>

          <ActionButton
            onClick={() => handleCommand('optimizer', 'Optimización genética')}
            disabled={isLoading}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <Zap size={20} />
            Optimizar Layout
          </ActionButton>

          <ActionButton
            onClick={() => handleCommand('ml_optimizer', 'Optimización con ML')}
            disabled={isLoading}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <Brain size={20} />
            Optimizar con ML
          </ActionButton>

          <ActionButton
            variant="success"
            onClick={() => handleCommand('remapper', 'Aplicar layout')}
            disabled={isLoading}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <Keyboard size={20} />
            Aplicar Layout
          </ActionButton>

          <ActionButton
            variant="warning"
            onClick={() => handleCommand('overlay', 'Lanzar overlay')}
            disabled={isLoading}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <Eye size={20} />
            Lanzar Overlay
          </ActionButton>

          <div style={{ marginTop: '30px' }}>
            <h3 style={{ color: 'white', marginBottom: '15px' }}>Estado del Sistema</h3>
            
            <StatusIndicator>
              <Activity size={16} />
              <span>Keylogger: {status.keylogger ? '✅ Activo' : '❌ Inactivo'}</span>
            </StatusIndicator>
            
            <StatusIndicator>
              <BarChart3 size={16} />
              <span>Analizador: {status.analyzer ? '✅ Completado' : '❌ Pendiente'}</span>
            </StatusIndicator>
            
            <StatusIndicator>
              <Zap size={16} />
              <span>Optimizador: {status.optimizer ? '✅ Completado' : '❌ Pendiente'}</span>
            </StatusIndicator>
            
            <StatusIndicator>
              <Keyboard size={16} />
              <span>Remapper: {status.remapper ? '✅ Activo' : '❌ Inactivo'}</span>
            </StatusIndicator>
          </div>
        </ControlPanel>

        <VisualizationPanel
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
        >
          <TabContainer>
            <Tab 
              active={activeTab === 'heatmap'} 
              onClick={() => setActiveTab('heatmap')}
            >
              Heatmap
            </Tab>
            <Tab 
              active={activeTab === 'optimized'} 
              onClick={() => setActiveTab('optimized')}
            >
              Layout Optimizado
            </Tab>
            <Tab 
              active={activeTab === 'logs'} 
              onClick={() => setActiveTab('logs')}
            >
              Logs
            </Tab>
          </TabContainer>

          <AnimatePresence mode="wait">
            {activeTab === 'heatmap' && (
              <motion.div
                key="heatmap"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
              >
                <KeyboardHeatmap />
              </motion.div>
            )}
            
            {activeTab === 'optimized' && (
              <motion.div
                key="optimized"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
              >
                <OptimizedLayout />
              </motion.div>
            )}
            
            {activeTab === 'logs' && (
              <motion.div
                key="logs"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
              >
                <LogViewer logs={logs} />
              </motion.div>
            )}
          </AnimatePresence>
        </VisualizationPanel>
      </MainContent>

      <AnimatePresence>
        {notification && (
          <Notification
            type={notification.type}
            initial={{ opacity: 0, x: 300 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 300 }}
            transition={{ duration: 0.3 }}
          >
            {notification.type === 'success' && <CheckCircle size={20} />}
            {notification.type === 'error' && <AlertCircle size={20} />}
            {notification.type === 'warning' && <AlertCircle size={20} />}
            {notification.type === 'info' && <Activity size={20} />}
            {notification.message}
            <X 
              size={16} 
              style={{ marginLeft: 'auto', cursor: 'pointer' }}
              onClick={() => setNotification(null)}
            />
          </Notification>
        )}
      </AnimatePresence>
    </AppContainer>
  );
}

export default App; 