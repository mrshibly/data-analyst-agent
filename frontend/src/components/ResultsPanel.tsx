import { useRef, useEffect, useState } from 'react';
import type { AnalysisResponse, ChartInfo, StatisticsInfo } from '../types';
import ChartViewer from './ChartViewer';
import { Terminal, BrainCircuit, BarChart3, LineChart, AlertTriangle, ChevronDown, ChevronUp } from 'lucide-react';

interface ResultsPanelProps {
  result: AnalysisResponse | null;
  isLoading: boolean;
  error: string | null;
  streamingLogs?: string[];
  partialCharts?: ChartInfo[];
  partialStats?: StatisticsInfo | null;
}

export default function ResultsPanel({ 
  result, 
  isLoading, 
  error, 
  streamingLogs = [] 
}: ResultsPanelProps) {
  const [showLogs, setShowLogs] = useState(true);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current && isLoading) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [streamingLogs, isLoading]);

  if (error) {
    return (
      <div className="agent-message-card" style={{ border: '1px solid rgba(244, 114, 182, 0.4)', background: 'rgba(244, 114, 182, 0.05)' }}>
        <div style={{ color: 'var(--accent-pink)', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <AlertTriangle size={20} />
          <span>Analysis Failure: {error}</span>
        </div>
      </div>
    );
  }

  if (!result && !isLoading && streamingLogs.length === 0) return null;

  return (
    <div className="agent-message-card animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Reasoning Log Accordion */}
      {(streamingLogs.length > 0 || isLoading) && (
        <div style={{ background: 'var(--bg-input)', border: '1px solid var(--border)', borderRadius: 'var(--radius-md)', overflow: 'hidden' }}>
          <div 
            onClick={() => setShowLogs(!showLogs)}
            style={{ 
              padding: '0.75rem 1rem', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'space-between', 
              cursor: 'pointer',
              background: 'rgba(255, 255, 255, 0.02)'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
              <Terminal size={16} style={{ color: 'var(--accent-cyan)' }} />
              <span style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--accent-cyan)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                {isLoading ? 'Agent Reasoning & Tool Execution...' : 'Execution Trail & Reasoning'}
              </span>
            </div>
            {showLogs ? <ChevronUp size={16} style={{ color: 'var(--text-muted)' }} /> : <ChevronDown size={16} style={{ color: 'var(--text-muted)' }} />}
          </div>

          {showLogs && (
            <div 
              ref={scrollRef} 
              style={{ 
                padding: '1rem 1.25rem', 
                borderTop: '1px solid var(--border)', 
                maxHeight: '180px', 
                overflowY: 'auto', 
                fontFamily: "'JetBrains Mono', monospace", 
                fontSize: '0.82rem'
              }}
            >
               {streamingLogs.map((log, i) => (
                  <div key={i} style={{ marginBottom: '0.4rem', color: 'var(--text-dim)' }}>
                    <span style={{ color: 'var(--accent-cyan)', marginRight: '0.5rem' }}>→</span> {log}
                  </div>
               ))}
            </div>
          )}
        </div>
      )}

      {/* Intelligence Synthesis Summary */}
      {(result?.summary || (isLoading && !result)) && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <BrainCircuit size={20} style={{ color: 'var(--primary)' }} />
            <h3 style={{ fontSize: '0.85rem', color: 'var(--primary)', textTransform: 'uppercase', letterSpacing: '0.1em', fontWeight: 800 }}>
              Analytical Synthesis
            </h3>
          </div>
          <div style={{ fontSize: '1.08rem', lineHeight: 1.65, color: 'var(--text-main)', fontWeight: 500 }}>
            {result?.summary || "Synthesizing intelligence and processing dataset aggregation..."}
          </div>
        </div>
      )}

      {/* Interactive Visualizations */}
      {result?.charts && result.charts.length > 0 && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', marginTop: '0.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <BarChart3 size={20} style={{ color: 'var(--accent-cyan)' }} />
            <h3 style={{ fontSize: '0.85rem', color: 'var(--accent-cyan)', textTransform: 'uppercase', letterSpacing: '0.1em', fontWeight: 800 }}>
              Visual Intelligence
            </h3>
          </div>
          <ChartViewer charts={result.charts} />
        </div>
      )}

      {/* Key Insights Grid */}
      {result?.insights && result.insights.length > 0 && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', marginTop: '0.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <LineChart size={20} style={{ color: 'var(--accent-pink)' }} />
            <h3 style={{ fontSize: '0.85rem', color: 'var(--accent-pink)', textTransform: 'uppercase', letterSpacing: '0.1em', fontWeight: 800 }}>
              Key Insights
            </h3>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem' }}>
             {result.insights.map((insight, i) => (
                <div 
                  key={i} 
                  style={{ 
                    padding: '1.15rem', 
                    background: 'rgba(99, 102, 241, 0.05)', 
                    borderRadius: 'var(--radius-md)', 
                    borderLeft: '4px solid var(--primary)', 
                    borderTop: '1px solid var(--border)',
                    borderRight: '1px solid var(--border)',
                    borderBottom: '1px solid var(--border)',
                    fontSize: '0.92rem',
                    lineHeight: 1.55,
                    color: 'var(--text-main)'
                  }}
                >
                  {insight}
                </div>
             ))}
          </div>
        </div>
      )}
    </div>
  );
}
