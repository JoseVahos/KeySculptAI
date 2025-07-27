import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { Zap, RefreshCw, Download, TrendingUp } from 'lucide-react';
import { getOptimizedLayout } from '../services/api';

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

const LayoutContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 30px;
`;

const Row = styled.div`
  display: flex;
  justify-content: center;
  gap: 8px;
`;

const Key = styled(motion.div)`
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: ${props => {
    if (props.isOptimized) {
      const intensity = props.frequency || 0;
      const maxFreq = props.maxFrequency || 1;
      const alpha = 0.3 + (intensity / maxFreq) * 0.7;
      return `rgba(34, 197, 94, ${alpha})`;
    }
    return 'rgba(255, 255, 255, 0.1)';
  }};
  border: 2px solid ${props => props.isOptimized ? 'rgba(34, 197, 94, 0.5)' : 'rgba(255, 255, 255, 0.2)'};
  border-radius: 8px;
  font-weight: 600;
  font-size: 1.1rem;
  cursor: pointer;
  position: relative;
  
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

const ComparisonSection = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-top: 30px;
`;

const LayoutSection = styled.div`
  background: rgba(255, 255, 255, 0.05);
  padding: 20px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
`;

const SectionTitle = styled.h4`
  font-size: 1.2rem;
  margin-bottom: 15px;
  text-align: center;
  color: ${props => props.variant === 'optimized' ? '#22c55e' : '#fbbf24'};
`;

const Stats = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
  margin-top: 20px;
`;

const StatCard = styled.div`
  background: rgba(255, 255, 255, 0.1);
  padding: 15px;
  border-radius: 8px;
  text-align: center;
`;

const StatValue = styled.div`
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 5px;
  color: ${props => props.color || 'white'};
`;

const StatLabel = styled.div`
  font-size: 0.8rem;
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

const OptimizedLayout = () => {
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
      const layoutData = await getOptimizedLayout();
      setData(layoutData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const getKeyFrequency = (key) => {
    if (!data || !data.frequencies) return 0;
    return data.frequencies[key] || 0;
  };

  const getMaxFrequency = () => {
    if (!data || !data.frequencies) return 0;
    return Math.max(...Object.values(data.frequencies));
  };

  const getOptimizationStats = () => {
    if (!data) return {};
    
    const totalKeys = 26;
    const optimizedKeys = data.layout ? data.layout.flat().length : 0;
    const improvement = data.improvement || 0;
    
    return {
      optimizedKeys,
      improvement: Math.round(improvement * 100) / 100,
      efficiency: Math.round((optimizedKeys / totalKeys) * 100)
    };
  };

  if (loading) {
    return (
      <Container>
        <LoadingSpinner>
          <RefreshCw size={24} style={{ animation: 'spin 1s linear infinite' }} />
          <span style={{ marginLeft: '10px' }}>Cargando layout optimizado...</span>
        </LoadingSpinner>
      </Container>
    );
  }

  if (error) {
    return (
      <Container>
        <ErrorMessage>
          <p>Error al cargar el layout optimizado: {error}</p>
          <Button onClick={fetchData} style={{ marginTop: '10px' }}>
            <RefreshCw size={16} />
            Reintentar
          </Button>
        </ErrorMessage>
      </Container>
    );
  }

  if (!data || !data.layout) {
    return (
      <Container>
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <p>No hay layout optimizado disponible. Ejecuta el optimizador primero.</p>
        </div>
      </Container>
    );
  }

  const stats = getOptimizationStats();
  const maxFreq = getMaxFrequency();

  return (
    <Container>
      <Header>
        <Title>
          <Zap size={24} />
          Layout Optimizado
        </Title>
        <Controls>
          <Button onClick={fetchData} whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
            <RefreshCw size={16} />
            Actualizar
          </Button>
        </Controls>
      </Header>

      <ComparisonSection>
        <LayoutSection>
          <SectionTitle variant="original">Layout QWERTY Original</SectionTitle>
          <LayoutContainer>
            {qwertyLayout.map((row, rowIndex) => (
              <Row key={rowIndex}>
                {row.map((key) => (
                  <Key
                    key={key}
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    {key.toUpperCase()}
                    <KeyTooltip>
                      {key.toUpperCase()}: {getKeyFrequency(key)} pulsaciones
                    </KeyTooltip>
                  </Key>
                ))}
              </Row>
            ))}
          </LayoutContainer>
        </LayoutSection>

        <LayoutSection>
          <SectionTitle variant="optimized">Layout Optimizado</SectionTitle>
          <LayoutContainer>
            {data.layout.map((row, rowIndex) => (
              <Row key={rowIndex}>
                {row.map((key) => (
                  <Key
                    key={key}
                    isOptimized={true}
                    frequency={getKeyFrequency(key)}
                    maxFrequency={maxFreq}
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    {key.toUpperCase()}
                    <KeyTooltip>
                      {key.toUpperCase()}: {getKeyFrequency(key)} pulsaciones
                    </KeyTooltip>
                  </Key>
                ))}
              </Row>
            ))}
          </LayoutContainer>
        </LayoutSection>
      </ComparisonSection>

      <Stats>
        <StatCard>
          <StatValue color="#22c55e">{stats.optimizedKeys}</StatValue>
          <StatLabel>Teclas Optimizadas</StatLabel>
        </StatCard>
        <StatCard>
          <StatValue color="#fbbf24">{stats.improvement}%</StatValue>
          <StatLabel>Mejora de Eficiencia</StatLabel>
        </StatCard>
        <StatCard>
          <StatValue color="#3b82f6">{stats.efficiency}%</StatValue>
          <StatLabel>Eficiencia Total</StatLabel>
        </StatCard>
        <StatCard>
          <StatValue color="#ef4444">{Math.round(maxFreq)}</StatValue>
          <StatLabel>Máxima Frecuencia</StatLabel>
        </StatCard>
      </Stats>
    </Container>
  );
};

export default OptimizedLayout; 