import { useEffect, useRef } from 'react';
import type { ChartInfo } from '../types';
import { getChartUrl } from '../services/api';

interface ChartViewerProps {
  charts: ChartInfo[];
}

/**
 * A native, zero-dependency Plotly component that uses the CDN-loaded library.
 */
function Plot({ data, layout, config }: any) {
  const chartRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const Plotly = (window as any).Plotly;
    if (chartRef.current && Plotly) {
      // Create the plot
      Plotly.newPlot(chartRef.current, data, layout, config);
      
      // Handle responsiveness
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

export default function ChartViewer({ charts }: ChartViewerProps) {
  if (charts.length === 0) return null;

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem', marginTop: '1.5rem' }}>
      {charts.map((chart, i) => (
        <div key={i} className="glass-pane" style={{ padding: '1.5rem', background: 'rgba(var(--background-rgb), 0.5)' }}>
          <div style={{ borderRadius: 'var(--radius-sm)', overflow: 'hidden' }}>
            {chart.plotly_data ? (
              <Plot
                data={chart.plotly_data.data || []}
                layout={{
                  ...chart.plotly_data.layout,
                  autosize: true,
                  paper_bgcolor: 'rgba(0,0,0,0)',
                  plot_bgcolor: 'rgba(0,0,0,0)',
                  font: { color: 'white', family: 'Inter, system-ui, sans-serif' },
                  margin: { l: 40, r: 20, t: 40, b: 40 },
                  height: 350,
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
          <div style={{ marginTop: '1.25rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <span style={{ fontWeight: 600, fontSize: '0.95rem', color: 'var(--text-primary)' }}>{chart.title}</span>
            <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              {chart.chart_type || 'Visualization'}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}
