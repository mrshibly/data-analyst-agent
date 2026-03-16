import type { UploadResponse } from '../types';
import { Database } from 'lucide-react';

interface DataPreviewProps {
  data: UploadResponse | null;
}

export default function DataPreview({ data }: DataPreviewProps) {
  if (!data || data.preview.length === 0) return null;

  const columns = data.columns.map(c => c.name);

  return (
    <div className="glass-pane animate-fade-in" style={{ padding: '0', overflow: 'hidden' }}>
      <div className="data-preview-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <Database size={16} style={{ color: 'var(--primary)' }} />
          <h3 style={{ fontSize: '0.75rem', color: 'var(--primary)', textTransform: 'uppercase', letterSpacing: '0.15em' }}>Knowledge Base Preview</h3>
        </div>
        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
          <strong style={{ color: 'var(--text-main)', wordBreak: 'break-all' }}>{data.filename}</strong>
        </div>
      </div>

      <div style={{ overflowX: 'auto', width: '100%', maxWidth: '100%' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem', textAlign: 'left' }}>
          <thead>
            <tr>
              <th style={{ padding: '1rem 1.5rem', background: 'rgba(255,255,255,0.02)', color: 'var(--text-muted)', fontWeight: 600, borderBottom: '1px solid var(--border)', width: '50px' }}>#</th>
              {columns.map((col) => (
                <th key={col} style={{ padding: '1rem 1.5rem', background: 'rgba(255,255,255,0.02)', color: 'var(--text-main)', fontWeight: 700, borderBottom: '1px solid var(--border)', whiteSpace: 'nowrap' }}>
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.preview.map((row, i) => (
              <tr key={i} style={{ borderBottom: '1px solid var(--border)', transition: 'background 0.2s ease' }}>
                <td style={{ padding: '0.85rem 1.5rem', color: 'var(--text-muted)', fontSize: '0.75rem' }}>{i + 1}</td>
                {columns.map((col) => (
                  <td key={col} style={{ padding: '0.85rem 1.5rem', color: 'var(--text-dim)', whiteSpace: 'nowrap' }}>
                    {String(row[col] ?? '')}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

