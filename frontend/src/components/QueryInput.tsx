import { useState } from 'react';
import { Send, Loader2, Sparkles, Trophy, TrendingUp, BarChart2, AlertCircle } from 'lucide-react';

interface QueryInputProps {
  onSubmit: (query: string) => void;
  isLoading: boolean;
  disabled: boolean;
}

const QUICK_SUGGESTIONS = [
  { icon: Trophy, label: 'Top Scorers', prompt: 'Who are the top 5 goalscorers across all leagues? Create a bar chart.' },
  { icon: TrendingUp, label: 'Rating vs Value', prompt: 'What is the correlation between player rating and market value in EUR?' },
  { icon: BarChart2, label: 'Goals by League', prompt: 'Compare total goals scored by Premier League vs La Liga players.' },
  { icon: AlertCircle, label: 'Outliers & Anomalies', prompt: 'Identify players with high ratings but lower market values.' }
];

export default function QueryInput({ onSubmit, isLoading, disabled }: QueryInputProps) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim() && !isLoading && !disabled) {
      onSubmit(query.trim());
      setQuery('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="sticky-input-bar">
      {/* Quick Suggestions Pills */}
      {!disabled && (
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', justifyContent: 'center', marginBottom: '0.75rem', maxWidth: '900px' }}>
          {QUICK_SUGGESTIONS.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.label}
                type="button"
                onClick={() => {
                  setQuery(item.prompt);
                }}
                disabled={isLoading}
                style={{
                  padding: '0.35rem 0.85rem',
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  background: 'rgba(15, 23, 42, 0.8)',
                  border: '1px solid var(--border)',
                  borderRadius: '100px',
                  color: 'var(--text-dim)',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.4rem',
                  transition: 'all 0.2s ease',
                  backdropFilter: 'blur(10px)'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.borderColor = 'var(--primary)';
                  e.currentTarget.style.color = '#fff';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.borderColor = 'var(--border)';
                  e.currentTarget.style.color = 'var(--text-dim)';
                }}
              >
                <Icon size={13} style={{ color: 'var(--accent-cyan)' }} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>
      )}

      {/* Floating Input Box */}
      <form onSubmit={handleSubmit} style={{ width: '100%', display: 'flex', justifyContent: 'center' }}>
        <div className="input-box-wrapper">
          <Sparkles size={18} style={{ color: 'var(--primary)' }} />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={disabled ? 'Upload a dataset to enable AI data analysis...' : 'Ask Lumina Analyst anything about your dataset...'}
            disabled={disabled || isLoading}
            style={{
              flex: 1,
              background: 'transparent',
              border: 'none',
              outline: 'none',
              color: 'var(--text-main)',
              fontSize: '0.98rem',
              fontWeight: 500
            }}
          />

          <button
            type="submit"
            disabled={!query.trim() || isLoading || disabled}
            style={{
              padding: '0.55rem 1.25rem',
              background: 'linear-gradient(135deg, var(--primary), var(--primary-hover))',
              color: 'white',
              border: 'none',
              borderRadius: '100px',
              fontWeight: 700,
              fontSize: '0.85rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              cursor: 'pointer',
              opacity: (query.trim() && !isLoading && !disabled) ? 1 : 0.4,
              boxShadow: '0 4px 15px var(--primary-glow)',
              transition: 'all 0.2s ease'
            }}
          >
            {isLoading ? <Loader2 className="animate-spin" size={16} /> : <Send size={16} />}
            <span>{isLoading ? 'Analyzing' : 'Send'}</span>
          </button>
        </div>
      </form>
    </div>
  );
}
