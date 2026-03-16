import { useState } from 'react';
import { Send, Sparkles, Loader2 } from 'lucide-react';

interface QueryInputProps {
  onSubmit: (query: string) => void;
  isLoading: boolean;
  disabled: boolean;
}

const SAMPLE_PROMPTS = [
  'Summarize the core patterns',
  'Find top correlations',
  'Analyze distribution of values',
  'Show trends and outliers',
  'Predict upcoming cycles',
  'Identify anomalies',
  'Compare segments',
  'Growth drivers'
];

export default function QueryInput({ onSubmit, isLoading, disabled }: QueryInputProps) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim() && !isLoading && !disabled) {
      onSubmit(query.trim());
    }
  };

  return (
    <div className="glass-pane animate-fade-in query-input-container">
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.25rem' }}>
        <Sparkles size={18} style={{ color: 'var(--primary)' }} />
        <h2 style={{ fontSize: '0.85rem', color: 'var(--primary)', textTransform: 'uppercase', letterSpacing: '0.15em', fontWeight: 800 }}>Analytical Inquiry</h2>
      </div>

      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={disabled ? 'Awaiting knowledge source...' : 'Ask the agent to analyze your data...'}
          disabled={disabled || isLoading}
          style={{
            width: '100%',
            padding: '1.25rem',
            background: 'var(--bg-subtle)',
            border: '1px solid var(--border)',
            borderRadius: 'var(--radius-md)',
            color: 'var(--text-main)',
            fontFamily: 'inherit',
            fontSize: '1rem',
            lineHeight: '1.5',
            resize: 'none',
            minHeight: '140px',
            transition: 'all 0.3s ease'
          }}
          onFocus={(e) => e.target.style.borderColor = 'var(--primary)'}
          onBlur={(e) => e.target.style.borderColor = 'var(--border)'}
        />

        <div className="query-input-footer">
          <div className="sample-prompts">
            {SAMPLE_PROMPTS.map((prompt) => (
              <button
                key={prompt}
                type="button"
                onClick={() => setQuery(prompt)}
                disabled={disabled || isLoading}
                style={{
                  padding: '0.35rem 0.75rem',
                  fontSize: '0.7rem',
                  background: 'rgba(255,255,255,0.03)',
                  border: '1px solid var(--border)',
                  borderRadius: '100px',
                  color: 'var(--text-dim)',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  whiteSpace: 'nowrap'
                }}
              >
                {prompt}
              </button>
            ))}
          </div>

          <button
            type="submit"
            disabled={!query.trim() || isLoading || disabled}
            style={{
              padding: '0.6rem 1.25rem',
              background: 'linear-gradient(135deg, var(--primary), #4f46e5)',
              color: 'white',
              border: 'none',
              borderRadius: '100px',
              fontWeight: 700,
              fontSize: '0.85rem',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '0.6rem',
              cursor: 'pointer',
              opacity: (query.trim() && !isLoading && !disabled) ? 1 : 0.5,
              boxShadow: '0 4px 15px var(--primary-glow)',
              width: '100%',
              maxWidth: '120px'
            }}
          >
            {isLoading ? <Loader2 className="animate-spin" size={16} /> : <Send size={16} />}
            <span>{isLoading ? 'Processing' : 'Analyze'}</span>
          </button>
        </div>
      </form>
    </div>
  );
}
