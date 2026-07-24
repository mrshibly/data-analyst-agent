import type { ReactNode } from 'react';
import type { UploadResponse } from '../types';
import { Sparkles, FileSpreadsheet, Download, RotateCcw } from 'lucide-react';

interface LayoutProps {
  children: ReactNode;
  activeData: UploadResponse | null;
  onOpenDrawer: () => void;
  onResetData: () => void;
  onExportReport?: () => void;
}

export default function Layout({ children, activeData, onOpenDrawer, onResetData, onExportReport }: LayoutProps) {
  return (
    <div className="layout-root">
      {/* Top Header Bar */}
      <header 
        style={{ 
          height: '60px',
          background: 'var(--bg-header)',
          backdropFilter: 'var(--glass-blur)',
          borderBottom: '1px solid var(--border)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '0 1.5rem',
          position: 'sticky',
          top: 0,
          zIndex: 100
        }}
      >
        {/* Brand */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
          <div style={{ 
            width: '36px', 
            height: '36px', 
            background: 'linear-gradient(135deg, var(--primary), var(--accent-cyan))', 
            borderRadius: '10px', 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center', 
            color: 'white',
            boxShadow: '0 4px 14px var(--primary-glow)'
          }}>
            <Sparkles size={18} />
          </div>
          <span style={{ fontSize: '1.15rem', fontWeight: 800, color: 'var(--text-main)', letterSpacing: '-0.02em' }}>
            Lumina Analyst
          </span>
        </div>

        {/* Active Dataset & Actions */}
        {activeData && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <button
              onClick={onOpenDrawer}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                padding: '0.4rem 0.9rem',
                background: 'rgba(99, 102, 241, 0.1)',
                border: '1px solid rgba(99, 102, 241, 0.3)',
                borderRadius: '100px',
                color: 'var(--text-main)',
                fontSize: '0.8rem',
                fontWeight: 600,
                cursor: 'pointer',
                transition: 'all 0.2s ease'
              }}
            >
              <FileSpreadsheet size={15} style={{ color: 'var(--accent-cyan)' }} />
              <span>{activeData.filename}</span>
              <span style={{ color: 'var(--text-muted)' }}>•</span>
              <span style={{ color: 'var(--accent-cyan)' }}>{activeData.row_count} rows</span>
            </button>

            {onExportReport && (
              <button
                onClick={onExportReport}
                title="Export Analytical Report"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.4rem',
                  padding: '0.4rem 0.85rem',
                  background: 'linear-gradient(135deg, var(--primary), var(--primary-hover))',
                  border: 'none',
                  borderRadius: '100px',
                  color: 'white',
                  fontSize: '0.78rem',
                  fontWeight: 700,
                  cursor: 'pointer',
                  boxShadow: '0 4px 14px var(--primary-glow)'
                }}
              >
                <Download size={14} />
                <span>Export Report</span>
              </button>
            )}

            <button
              onClick={onResetData}
              title="Switch Dataset"
              style={{
                padding: '0.4rem 0.75rem',
                background: 'rgba(255, 255, 255, 0.04)',
                border: '1px solid var(--border)',
                borderRadius: '100px',
                color: 'var(--text-dim)',
                fontSize: '0.78rem',
                fontWeight: 600,
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '0.35rem'
              }}
            >
              <RotateCcw size={14} />
              <span>Reset</span>
            </button>
          </div>
        )}
      </header>

      {/* Main Workspace Container */}
      <div style={{ flex: 1, position: 'relative' }}>
        {children}
      </div>
    </div>
  );
}
