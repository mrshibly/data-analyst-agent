import type { ReactNode } from 'react';
import { ShieldCheck, Zap } from 'lucide-react';

interface LayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  return (
    <div className="layout-root">
      <header className="glass-pane" style={{ 
        margin: '1rem', 
        borderRadius: 'var(--radius-md)', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'space-between',
        padding: '1rem 2rem'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
          <div style={{ 
            width: '44px', 
            height: '44px', 
            background: 'linear-gradient(135deg, var(--primary), #4f46e5)', 
            borderRadius: '12px', 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center', 
            color: 'white',
            fontWeight: 800,
            fontSize: '1.2rem',
            position: 'relative'
          }}>
            DA
            <div style={{ position: 'absolute', inset: '-4px', background: 'var(--primary)', filter: 'blur(12px)', opacity: 0.3, zIndex: -1 }} />
          </div>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <span className="brand-text" style={{ fontSize: '1.3rem', lineHeight: 1.1 }}>Lumina Analyst</span>
            <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.15em', fontWeight: 600 }}>Advanced Data Intelligence</span>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '2rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', padding: '0.5rem 1rem', background: 'rgba(255, 255, 255, 0.03)', border: '1px solid var(--border)', borderRadius: '100px' }}>
            <div style={{ width: '8px', height: '8px', background: 'var(--accent)', borderRadius: '50%', boxShadow: '0 0 10px var(--accent)' }} className="animate-pulse" />
            <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-dim)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Engine Synced</span>
          </div>
          <div style={{ display: 'flex', gap: '1rem' }}>
             <ShieldCheck size={20} style={{ color: 'var(--text-muted)', cursor: 'pointer' }} />
             <Zap size={20} style={{ color: 'var(--text-muted)', cursor: 'pointer' }} />
          </div>
        </div>
      </header>

      <main style={{ flex: 1, padding: '1rem 2rem', maxWidth: '1400px', margin: '0 auto', width: '100%' }}>
        {children}
      </main>

      <footer style={{ padding: '2rem', textAlign: 'center', borderTop: '1px solid var(--border)', marginTop: '4rem' }}>
        <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>&copy; 2026 Lumina Insight Hub. Secure Neural Analysis Environment.</p>
      </footer>
    </div>
  );
}
