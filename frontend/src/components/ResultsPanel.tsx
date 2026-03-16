import { useRef, useEffect } from 'react';
import type { AnalysisResponse, ChartInfo, StatisticsInfo } from '../types';
import ChartViewer from './ChartViewer';
import { Terminal, BrainCircuit, BarChart3, LineChart } from 'lucide-react';

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
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current && isLoading) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [streamingLogs, isLoading]);

  if (error) {
    return (
      <div className="glass-pane animate-fade-in" style={{ borderColor: 'rgba(244, 114, 182, 0.3)' }}>
        <div style={{ color: '#f472b6', fontWeight: 600 }}>⚠️ Analysis Failed: {error}</div>
      </div>
    );
  }

  if (!result && !isLoading && streamingLogs.length === 0) return null;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }} className="animate-fade-in">
      {/* Reasoning Feed */}
      {isLoading && (
        <div className="glass-pane">
           <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.25rem' }}>
            <Terminal size={18} style={{ color: 'var(--accent)' }} />
            <h3 style={{ fontSize: '0.8rem', color: 'var(--accent)', textTransform: 'uppercase', letterSpacing: '0.15em' }}>Agent Reasoning</h3>
          </div>
          <div ref={scrollRef} style={{ background: 'rgba(0,0,0,0.3)', padding: '1.25rem', borderRadius: '8px', maxHeight: '200px', overflowY: 'auto', fontFamily: 'monospace', fontSize: '0.85rem' }}>
             {streamingLogs.map((log, i) => (
                <div key={i} style={{ marginBottom: '0.4rem', color: 'var(--text-dim)' }}>
                  <span style={{ color: 'var(--primary)', marginRight: '0.75rem' }}>→</span> {log}
                </div>
             ))}
          </div>
        </div>
      )}

      {/* Synthesis */}
      {(result?.summary || (isLoading && !result)) && (
        <div className="glass-pane">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.5rem' }}>
            <BrainCircuit size={20} style={{ color: 'var(--primary)' }} />
            <h3 style={{ fontSize: '0.8rem', color: 'var(--primary)', textTransform: 'uppercase', letterSpacing: '0.15em' }}>Intelligence Synthesis</h3>
          </div>
          <div style={{ fontSize: '1.15rem', lineHeight: 1.6, color: 'var(--text-main)' }}>
            {result?.summary || "Synthesizing analytical intelligence..."}
          </div>
        </div>
      )}

      {/* Visuals */}
      {result?.charts && result.charts.length > 0 && (
        <div className="glass-pane">
           <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.5rem' }}>
            <BarChart3 size={20} style={{ color: 'var(--primary)' }} />
            <h3 style={{ fontSize: '0.8rem', color: 'var(--primary)', textTransform: 'uppercase', letterSpacing: '0.15em' }}>Visual Intelligence</h3>
          </div>
          <ChartViewer charts={result.charts} />
        </div>
      )}

      {/* Insights */}
      {result?.insights && result.insights.length > 0 && (
        <div className="glass-pane">
           <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.5rem' }}>
            <LineChart size={20} style={{ color: 'var(--primary)' }} />
            <h3 style={{ fontSize: '0.8rem', color: 'var(--primary)', textTransform: 'uppercase', letterSpacing: '0.15em' }}>Key Insights</h3>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.25rem' }}>
             {result.insights.map((insight, i) => (
                <div key={i} style={{ padding: '1.25rem', background: 'rgba(129, 140, 248, 0.05)', borderRadius: '12px', borderLeft: '3px solid var(--primary)', fontSize: '0.95rem' }}>
                  {insight}
                </div>
             ))}
          </div>
        </div>
      )}
    </div>
  );
}
