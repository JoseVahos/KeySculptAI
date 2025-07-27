import React, { useState, useRef, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FileText, Trash2, Download, Copy, CheckCircle } from 'lucide-react';

const Container = styled.div`
  color: white;
  height: 100%;
  display: flex;
  flex-direction: column;
`;

const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
`;

const Title = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 10px;
`;

const Controls = styled.div`
  display: flex;
  gap: 10px;
`;

const Button = styled(motion.button)`
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(255, 255, 255, 0.2);
  }
`;

const LogContainer = styled.div`
  flex: 1;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 12px;
  padding: 20px;
  overflow-y: auto;
  max-height: 500px;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 0.9rem;
  line-height: 1.5;
`;

const LogEntry = styled(motion.div)`
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 8px;
  padding: 8px;
  border-radius: 6px;
  background: ${props => {
    switch (props.type) {
      case 'success':
        return 'rgba(34, 197, 94, 0.1)';
      case 'error':
        return 'rgba(239, 68, 68, 0.1)';
      case 'warning':
        return 'rgba(245, 158, 11, 0.1)';
      default:
        return 'rgba(59, 130, 246, 0.1)';
    }
  }};
  border-left: 3px solid ${props => {
    switch (props.type) {
      case 'success':
        return '#22c55e';
      case 'error':
        return '#ef4444';
      case 'warning':
        return '#f59e0b';
      default:
        return '#3b82f6';
    }
  }};
`;

const Timestamp = styled.span`
  color: #9ca3af;
  font-size: 0.8rem;
  min-width: 80px;
`;

const Message = styled.span`
  flex: 1;
  color: ${props => {
    switch (props.type) {
      case 'success':
        return '#22c55e';
      case 'error':
        return '#ef4444';
      case 'warning':
        return '#f59e0b';
      default:
        return 'white';
    }
  }};
`;

const EmptyState = styled.div`
  text-align: center;
  padding: 40px;
  color: #9ca3af;
`;

const FilterContainer = styled.div`
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
  flex-wrap: wrap;
`;

const FilterButton = styled.button`
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  background: ${props => props.active ? 'rgba(255, 255, 255, 0.2)' : 'rgba(255, 255, 255, 0.1)'};
  color: white;
  cursor: pointer;
  font-size: 0.8rem;
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(255, 255, 255, 0.2);
  }
`;

const LogViewer = ({ logs }) => {
  const [filter, setFilter] = useState('all');
  const [copied, setCopied] = useState(false);
  const logContainerRef = useRef(null);

  const logTypes = [
    { key: 'all', label: 'Todos', count: logs.length },
    { key: 'info', label: 'Info', count: logs.filter(log => log.type === 'info').length },
    { key: 'success', label: 'Éxito', count: logs.filter(log => log.type === 'success').length },
    { key: 'warning', label: 'Advertencia', count: logs.filter(log => log.type === 'warning').length },
    { key: 'error', label: 'Error', count: logs.filter(log => log.type === 'error').length },
  ];

  const filteredLogs = filter === 'all' 
    ? logs 
    : logs.filter(log => log.type === filter);

  useEffect(() => {
    if (logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
    }
  }, [logs]);

  const clearLogs = () => {
    // Esta función se manejaría desde el componente padre
    console.log('Limpiar logs');
  };

  const downloadLogs = () => {
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
  };

  const copyLogs = async () => {
    const logText = logs.map(log => 
      `[${log.timestamp}] ${log.type.toUpperCase()}: ${log.message}`
    ).join('\n');
    
    try {
      await navigator.clipboard.writeText(logText);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Error al copiar logs:', err);
    }
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case 'success':
        return '✅';
      case 'error':
        return '❌';
      case 'warning':
        return '⚠️';
      default:
        return 'ℹ️';
    }
  };

  return (
    <Container>
      <Header>
        <Title>
          <FileText size={24} />
          Registro del Sistema
        </Title>
        <Controls>
          <Button onClick={copyLogs} whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
            {copied ? <CheckCircle size={16} /> : <Copy size={16} />}
            {copied ? 'Copiado' : 'Copiar'}
          </Button>
          <Button onClick={downloadLogs} whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
            <Download size={16} />
            Descargar
          </Button>
          <Button onClick={clearLogs} whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
            <Trash2 size={16} />
            Limpiar
          </Button>
        </Controls>
      </Header>

      <FilterContainer>
        {logTypes.map(({ key, label, count }) => (
          <FilterButton
            key={key}
            active={filter === key}
            onClick={() => setFilter(key)}
          >
            {label} ({count})
          </FilterButton>
        ))}
      </FilterContainer>

      <LogContainer ref={logContainerRef}>
        {filteredLogs.length === 0 ? (
          <EmptyState>
            <FileText size={48} style={{ marginBottom: '10px', opacity: 0.5 }} />
            <p>No hay logs para mostrar</p>
            {filter !== 'all' && (
              <p style={{ fontSize: '0.8rem', marginTop: '5px' }}>
                Cambia el filtro para ver más logs
              </p>
            )}
          </EmptyState>
        ) : (
          filteredLogs.map((log, index) => (
            <LogEntry
              key={index}
              type={log.type}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3, delay: index * 0.05 }}
            >
              <Timestamp>{log.timestamp}</Timestamp>
              <span>{getTypeIcon(log.type)}</span>
              <Message type={log.type}>{log.message}</Message>
            </LogEntry>
          ))
        )}
      </LogContainer>
    </Container>
  );
};

export default LogViewer; 