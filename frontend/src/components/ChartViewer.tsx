import type { ChartInfo } from '../types';
import { getChartUrl } from '../services/api';

interface ChartViewerProps {
  charts: ChartInfo[];
}

export default function ChartViewer({ charts }: ChartViewerProps) {
  if (charts.length === 0) return null;

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem', marginTop: '1.5rem' }}>
      {charts.map((chart, i) => (
        <div key={i} className="glass-pane" style={{ padding: '1.5rem', background: 'rgba(0,0,0,0.2)' }}>
          {chart.plotly_data ? (
            <div style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '2rem' }}>
               [ Interactive Chart Payload Received ]
            </div>
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
          <div style={{ marginTop: '1.25rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <span style={{ fontWeight: 600, fontSize: '0.95rem' }}>{chart.title}</span>
            <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              {chart.chart_type || 'Visualization'}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}
