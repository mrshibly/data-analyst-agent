import { useEffect, useRef, useState } from 'react';
import type { ChartInfo } from '../types';
import { getChartUrl } from '../services/api';
import { Download, Maximize2, X, BarChart2, TrendingUp, Circle, PieChart } from 'lucide-react';

interface ChartViewerProps {
  charts: ChartInfo[];
}

function Plot({ data, layout, config }: any) {
  const chartRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const Plotly = (window as any).Plotly;
    if (chartRef.current && Plotly) {
      Plotly.newPlot(chartRef.current, data, layout, config);
      
      const handleResize = () => {
        if (chartRef.current && Plotly) {
          Plotly.Plots.resize(chartRef.current);
        }
      };

      window.addEventListener('resize', handleResize);
      return () => window.removeEventListener('resize', handleResize);
    }
  }, [data, layout, config]);

  return <div ref={chartRef} style={{ width: '100%', borderRadius: 'inherit' }} />;
}

const PALETTES: Record<string, string[]> = {
  Indigo: ['#6366f1', '#38bdf8', '#a855f7', '#ec4899', '#10b981'],
  Emerald: ['#10b981', '#34d399', '#059669', '#38bdf8', '#fbbf24'],
  Sunset: ['#f97316', '#fbbf24', '#ef4444', '#a855f7', '#38bdf8'],
  Cyber: ['#06b6d4', '#8b5cf6', '#ec4899', '#3b82f6', '#10b981']
};

export default function ChartViewer({ charts }: ChartViewerProps) {
  const [activeChartType, setActiveChartType] = useState<Record<number, string>>({});
  const [selectedPalette] = useState<string>('Indigo');
  const [fullscreenChart, setFullscreenChart] = useState<ChartInfo | null>(null);

  if (charts.length === 0) return null;

  const downloadPng = (chartIndex: number, title: string) => {
    const Plotly = (window as any).Plotly;
    const el = document.getElementById(`plotly-chart-${chartIndex}`);
    if (Plotly && el) {
      Plotly.downloadImage(el, { format: 'png', width: 1200, height: 800, filename: title.replace(/\s+/g, '_') });
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', marginTop: '1rem' }}>
      {/* Fullscreen Chart Modal */}
      {fullscreenChart && (
        <div 
          style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.85)', backdropFilter: 'blur(10px)', zIndex: 300, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '2rem' }}
          onClick={() => setFullscreenChart(null)}
        >
          <div 
            style={{ width: '100%', maxWidth: '1100px', background: '#0f172a', border: '1px solid var(--border)', borderRadius: 'var(--radius-lg)', padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}
            onClick={(e) => e.stopPropagation()}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h3 style={{ fontSize: '1.3rem', color: '#fff', fontWeight: 800 }}>{fullscreenChart.title}</h3>
              <button onClick={() => setFullscreenChart(null)} style={{ background: 'none', border: 'none', color: 'var(--text-dim)', cursor: 'pointer' }}>
                <X size={24} />
              </button>
            </div>
            {fullscreenChart.plotly_data && (
              <Plot
                data={fullscreenChart.plotly_data.data || []}
                layout={{
                  ...fullscreenChart.plotly_data.layout,
                  autosize: true,
                  paper_bgcolor: 'rgba(0,0,0,0)',
                  plot_bgcolor: 'rgba(0,0,0,0)',
                  font: { color: 'white', family: 'Plus Jakarta Sans, sans-serif' },
                  margin: { l: 50, r: 30, t: 50, b: 50 },
                  height: 600,
                }}
                config={{ responsive: true }}
              />
            )}
          </div>
        </div>
      )}

      {/* Charts Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.5rem' }}>
        {charts.map((chart, i) => {
          const currentType = activeChartType[i] || chart.chart_type || 'bar';
          
          let modifiedPlotlyData = chart.plotly_data;
          if (modifiedPlotlyData && modifiedPlotlyData.data) {
            const colors = PALETTES[selectedPalette];
            const updatedTraces = modifiedPlotlyData.data.map((trace: any, idx: number) => ({
              ...trace,
              type: currentType === 'pie' ? 'pie' : (currentType === 'histogram' ? 'histogram' : (currentType === 'box' ? 'box' : (currentType === 'line' ? 'scatter' : trace.type))),
              mode: currentType === 'line' ? 'lines+markers' : (currentType === 'scatter' ? 'markers' : trace.mode),
              marker: {
                ...trace.marker,
                color: colors[idx % colors.length]
              }
            }));

            modifiedPlotlyData = {
              ...modifiedPlotlyData,
              data: updatedTraces
            };
          }

          return (
            <div key={i} className="glass-pane" style={{ padding: '1.25rem', background: '#0f172a', border: '1px solid var(--border)' }}>
              {/* Card Controls Header */}
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem', borderBottom: '1px solid var(--border)', paddingBottom: '0.75rem' }}>
                <span style={{ fontWeight: 700, fontSize: '0.95rem', color: 'var(--text-main)' }}>{chart.title}</span>

                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  {/* Chart Type Toggle Pill */}
                  {chart.plotly_data && (
                    <div style={{ display: 'flex', background: 'rgba(255, 255, 255, 0.05)', borderRadius: '100px', padding: '0.2rem', border: '1px solid var(--border)' }}>
                      <button title="Bar Chart" onClick={() => setActiveChartType(prev => ({ ...prev, [i]: 'bar' }))} style={{ background: currentType === 'bar' ? 'var(--primary)' : 'none', border: 'none', borderRadius: '50%', padding: '0.3rem', color: '#fff', cursor: 'pointer', display: 'flex' }}>
                        <BarChart2 size={13} />
                      </button>
                      <button title="Line Chart" onClick={() => setActiveChartType(prev => ({ ...prev, [i]: 'line' }))} style={{ background: currentType === 'line' ? 'var(--primary)' : 'none', border: 'none', borderRadius: '50%', padding: '0.3rem', color: '#fff', cursor: 'pointer', display: 'flex' }}>
                        <TrendingUp size={13} />
                      </button>
                      <button title="Scatter Chart" onClick={() => setActiveChartType(prev => ({ ...prev, [i]: 'scatter' }))} style={{ background: currentType === 'scatter' ? 'var(--primary)' : 'none', border: 'none', borderRadius: '50%', padding: '0.3rem', color: '#fff', cursor: 'pointer', display: 'flex' }}>
                        <Circle size={13} />
                      </button>
                      <button title="Pie Chart" onClick={() => setActiveChartType(prev => ({ ...prev, [i]: 'pie' }))} style={{ background: currentType === 'pie' ? 'var(--primary)' : 'none', border: 'none', borderRadius: '50%', padding: '0.3rem', color: '#fff', cursor: 'pointer', display: 'flex' }}>
                        <PieChart size={13} />
                      </button>
                    </div>
                  )}

                  {/* Actions */}
                  {chart.plotly_data && (
                    <button title="Download PNG" onClick={() => downloadPng(i, chart.title)} style={{ background: 'rgba(255, 255, 255, 0.05)', border: '1px solid var(--border)', borderRadius: '8px', padding: '0.35rem', color: 'var(--text-dim)', cursor: 'pointer', display: 'flex' }}>
                      <Download size={14} />
                    </button>
                  )}
                  {chart.plotly_data && (
                    <button title="Expand Fullscreen" onClick={() => setFullscreenChart(chart)} style={{ background: 'rgba(255, 255, 255, 0.05)', border: '1px solid var(--border)', borderRadius: '8px', padding: '0.35rem', color: 'var(--text-dim)', cursor: 'pointer', display: 'flex' }}>
                      <Maximize2 size={14} />
                    </button>
                  )}
                </div>
              </div>

              {/* Chart Plot Area */}
              <div id={`plotly-chart-${i}`} style={{ borderRadius: 'var(--radius-sm)', overflow: 'hidden' }}>
                {modifiedPlotlyData ? (
                  <Plot
                    data={modifiedPlotlyData.data || []}
                    layout={{
                      ...modifiedPlotlyData.layout,
                      autosize: true,
                      paper_bgcolor: 'rgba(0,0,0,0)',
                      plot_bgcolor: 'rgba(0,0,0,0)',
                      font: { color: 'white', family: 'Plus Jakarta Sans, sans-serif' },
                      margin: { l: 40, r: 20, t: 30, b: 40 },
                      height: 340,
                    }}
                    config={{ responsive: true, displayModeBar: false }}
                  />
                ) : (
                  chart.url && (
                    <img
                      src={getChartUrl(chart.url)}
                      alt={chart.title}
                      style={{ width: '100%', borderRadius: 'var(--radius-sm)', display: 'block' }}
                      loading="lazy"
                    />
                  )
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
