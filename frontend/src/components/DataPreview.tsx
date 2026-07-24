import type { UploadResponse } from '../types';
import { Database, Table } from 'lucide-react';

interface DataPreviewProps {
  data: UploadResponse | null;
}

export default function DataPreview({ data }: DataPreviewProps) {
  if (!data || data.preview.length === 0) return null;

  return (
    <div className="glass-pane animate-fade-in" style={{ padding: '0', overflow: 'hidden' }}>
      <div className="data-preview-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <Table size={18} style={{ color: 'var(--accent-cyan)' }} />
          <h3 style={{ fontSize: '0.85rem', color: 'var(--accent-cyan)', textTransform: 'uppercase', letterSpacing: '0.12em', fontWeight: 800 }}>
            Dataset Preview & Schema Inspection
          </h3>
        </div>
        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Database size={14} />
          <strong style={{ color: 'var(--text-main)', wordBreak: 'break-all' }}>{data.filename}</strong>
        </div>
      </div>

      <div style={{ overflowX: 'auto', width: '100%', maxWidth: '100%' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.88rem', textAlign: 'left' }}>
          <thead>
            <tr style={{ background: 'rgba(0, 0, 0, 0.4)' }}>
              <th style={{ padding: '1rem 1.25rem', color: 'var(--text-muted)', fontWeight: 700, borderBottom: '1px solid var(--border)', width: '50px' }}>#</th>
              {data.columns.map((col) => (
                <th key={col.name} style={{ padding: '1rem 1.25rem', color: 'var(--text-main)', fontWeight: 700, borderBottom: '1px solid var(--border)', whiteSpace: 'nowrap' }}>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.2rem' }}>
                    <span>{col.name}</span>
                    <span style={{ fontSize: '0.65rem', color: 'var(--accent-cyan)', textTransform: 'uppercase', letterSpacing: '0.05em', fontWeight: 600 }}>
                      {col.dtype}
                    </span>
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.preview.map((row, i) => (
              <tr 
                key={i} 
                style={{ 
                  borderBottom: '1px solid var(--border)', 
                  transition: 'background 0.2s ease',
                  background: i % 2 === 0 ? 'transparent' : 'rgba(255, 255, 255, 0.015)'
                }}
                onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(99, 102, 241, 0.08)'}
                onMouseLeave={(e) => e.currentTarget.style.background = i % 2 === 0 ? 'transparent' : 'rgba(255, 255, 255, 0.015)'}
              >
                <td style={{ padding: '0.85rem 1.25rem', color: 'var(--text-muted)', fontSize: '0.75rem', fontWeight: 700 }}>{i + 1}</td>
                {data.columns.map((col) => (
                  <td key={col.name} style={{ padding: '0.85rem 1.25rem', color: 'var(--text-dim)', whiteSpace: 'nowrap' }}>
                    {String(row[col.name] ?? '')}
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
