import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { BarChart3, Download, RefreshCw } from 'lucide-react';
import { getKeystrokesData } from '../services/api';

const Container = styled.div`
  color: white;
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

const KeyboardGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(10, 1fr);
  gap: 8px;
  max-width: 600px;
  margin: 0 auto;
`;

const Key = styled(motion.div)`
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: ${props => {
    const intensity = props.intensity || 0;
    const alpha = 0.1 + (intensity * 0.9);
    return `rgba(255, 107, 107, ${alpha})`;
  }};
  border-radius: 8px;
  font-weight: 600;
  font-size: 1.2rem;
  cursor: pointer;
  position: relative;
  border: 2px solid rgba(255, 255, 255, 0.1);
  
  &:hover {
    transform: scale(1.1);
    z-index: 10;
  }
`;

const KeyTooltip = styled.div`
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.9);
  color: white;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 0.8rem;
  white-space: nowrap;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.3s ease;
  
  ${Key}:hover & {
    opacity: 1;
  }
`;

const Stats = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 30px;
`;

const StatCard = styled.div`
  background: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: 12px;
  text-align: center;
`;

const StatValue = styled.div`
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 5px;
`;

const StatLabel = styled.div`
  font-size: 0.9rem;
  opacity: 0.8;
`;

const LoadingSpinner = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  font-size: 1.2rem;
  opacity: 0.7;
`;

const ErrorMessage = styled.div`
  background: rgba(239, 68, 68, 0.2);
  border: 1px solid rgba(239, 68, 68, 0.5);
  color: #fca5a5;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
`;

const KeyboardHeatmap = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const qwertyLayout = [
    ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
    ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
    ['z', 'x', 'c', 'v', 'b', 'n', 'm']
  ];

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const keystrokesData = await getKeystrokesData();
      setData(keystrokesData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const getKeyIntensity = (key) => {
    if (!data || !data.frequencies) return 0;
    return data.frequencies[key] || 0;
  };

  const getMaxFrequency = () => {
    if (!data || !data.frequencies) return 0;
    return Math.max(...Object.values(data.frequencies));
  };

  const getTotalKeystrokes = () => {
    if (!data || !data.frequencies) return 0;
    return Object.values(data.frequencies).reduce((sum, freq) => sum + freq, 0);
  };

  const getMostUsedKey = () => {
    if (!data || !data.frequencies) return 'N/A';
    const maxKey = Object.entries(data.frequencies).reduce((a, b) => 
      data.frequencies[a[0]] > data.frequencies[b[0]] ? a : b
    );
    return maxKey[0].toUpperCase();
  };

  if (loading) {
    return (
      <Container>
        <LoadingSpinner>
          <RefreshCw size={24} style={{ animation: 'spin 1s linear infinite' }} />
          <span style={{ marginLeft: '10px' }}>Cargando datos...</span>
        </LoadingSpinner>
      </Container>
    );
  }

  if (error) {
    return (
      <Container>
        <ErrorMessage>
          <p>Error al cargar los datos: {error}</p>
          <Button onClick={fetchData} style={{ marginTop: '10px' }}>
            <RefreshCw size={16} />
            Reintentar
          </Button>
        </ErrorMessage>
      </Container>
    );
  }

  if (!data) {
    return (
      <Container>
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <p>No hay datos disponibles. Ejecuta el keylogger para capturar datos.</p>
        </div>
      </Container>
    );
  }

  return (
    <Container>
      <Header>
        <Title>
          <BarChart3 size={24} />
          Heatmap de Frecuencias
        </Title>
        <Controls>
          <Button onClick={fetchData} whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
            <RefreshCw size={16} />
            Actualizar
          </Button>
        </Controls>
      </Header>

      <KeyboardGrid>
        {qwertyLayout.map((row, rowIndex) => 
          row.map((key, colIndex) => {
            const intensity = getKeyIntensity(key);
            const maxFreq = getMaxFrequency();
            const normalizedIntensity = maxFreq > 0 ? intensity / maxFreq : 0;
            
            return (
              <Key
                key={key}
                intensity={normalizedIntensity}
                style={{
                  gridColumn: rowIndex === 1 ? `${colIndex + 2} / span 1` : 
                              rowIndex === 2 ? `${colIndex + 3} / span 1` : 
                              `${colIndex + 1} / span 1`
                }}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
              >
                {key.toUpperCase()}
                <KeyTooltip>
                  {key.toUpperCase()}: {intensity} pulsaciones
                </KeyTooltip>
              </Key>
            );
          })
        )}
      </KeyboardGrid>

      <Stats>
        <StatCard>
          <StatValue>{getTotalKeystrokes()}</StatValue>
          <StatLabel>Total de Pulsaciones</StatLabel>
        </StatCard>
        <StatCard>
          <StatValue>{getMostUsedKey()}</StatValue>
          <StatLabel>Tecla Más Usada</StatLabel>
        </StatCard>
        <StatCard>
          <StatValue>{Object.keys(data.frequencies || {}).length}</StatValue>
          <StatLabel>Teclas Únicas</StatLabel>
        </StatCard>
        <StatCard>
          <StatValue>{Math.round(getMaxFrequency())}</StatValue>
          <StatLabel>Máxima Frecuencia</StatLabel>
        </StatCard>
      </Stats>
    </Container>
  );
};

export default KeyboardHeatmap; 