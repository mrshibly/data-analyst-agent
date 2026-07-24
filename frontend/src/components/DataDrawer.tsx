import type { UploadResponse } from '../types';
import { X, Table, FileSpreadsheet, Database } from 'lucide-react';

interface DataDrawerProps {
  data: UploadResponse | null;
  isOpen: boolean;
  onClose: () => void;
}

export default function DataDrawer({ data, isOpen, onClose }: DataDrawerProps) {
  if (!isOpen || !data) return null;

  return (
    <div className="drawer-overlay" onClick={onClose}>
      <div className="drawer-content" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid var(--border)', paddingBottom: '1.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <FileSpreadsheet size={24} style={{ color: 'var(--primary)' }} />
            <div>
              <h2 style={{ fontSize: '1.2rem', fontWeight: 800, color: 'var(--text-main)' }}>
                Dataset Inspection Drawer
              </h2>
              <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                {data.filename} • {data.row_count.toLocaleString()} rows • {data.column_count} columns
              </span>
            </div>
          </div>
          <button 
            onClick={onClose}
            style={{ 
              background: 'rgba(255, 255, 255, 0.05)', 
              border: '1px solid var(--border)', 
              borderRadius: '50%', 
              width: '36px', 
              height: '36px', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              color: 'var(--text-dim)',
              cursor: 'pointer'
            }}
          >
            <X size={18} />
          </button>
        </div>

        {/* Schema Breakdown Grid */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--accent-cyan)', fontSize: '0.85rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            <Database size={16} /> Column Schema & Data Types
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '0.75rem' }}>
            {data.columns.map((col) => (
              <div key={col.name} style={{ background: 'rgba(255, 255, 255, 0.02)', border: '1px solid var(--border)', padding: '0.75rem 1rem', borderRadius: 'var(--radius-md)', display: 'flex', flexDirection: 'column', gap: '0.2rem' }}>
                <span style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-main)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  {col.name}
                </span>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.72rem' }}>
                  <span style={{ color: 'var(--accent-cyan)', fontWeight: 600, textTransform: 'uppercase' }}>{col.dtype}</span>
                  <span style={{ color: 'var(--text-muted)' }}>{col.null_count === 0 ? 'No nulls' : `${col.null_count} nulls`}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Raw Data Preview Table */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--primary)', fontSize: '0.85rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            <Table size={16} /> Sample Rows Preview (First 5)
          </div>

          <div style={{ overflowX: 'auto', border: '1px solid var(--border)', borderRadius: 'var(--radius-md)', background: 'rgba(0, 0, 0, 0.2)' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem', textAlign: 'left' }}>
              <thead>
                <tr style={{ background: 'rgba(255, 255, 255, 0.04)', borderBottom: '1px solid var(--border)' }}>
                  <th style={{ padding: '0.85rem 1rem', color: 'var(--text-muted)' }}>#</th>
                  {data.columns.map((col) => (
                    <th key={col.name} style={{ padding: '0.85rem 1rem', color: 'var(--text-main)', fontWeight: 700, whiteSpace: 'nowrap' }}>
                      {col.name}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {data.preview.map((row, i) => (
                  <tr key={i} style={{ borderBottom: '1px solid var(--border)' }}>
                    <td style={{ padding: '0.75rem 1rem', color: 'var(--text-muted)', fontWeight: 700 }}>{i + 1}</td>
                    {data.columns.map((col) => (
                      <td key={col.name} style={{ padding: '0.75rem 1rem', color: 'var(--text-dim)', whiteSpace: 'nowrap' }}>
                        {String(row[col.name] ?? '')}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
