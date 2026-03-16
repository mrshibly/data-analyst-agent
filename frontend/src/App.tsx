import { useState, useCallback } from 'react';
import Layout from './components/Layout';
import FileUpload from './components/FileUpload';
import QueryInput from './components/QueryInput';
import ResultsPanel from './components/ResultsPanel';
import DataPreview from './components/DataPreview';
import { analyzeQueryStream } from './services/api';
import type { UploadResponse, AnalysisResponse, ChartInfo, StatisticsInfo, ChatMessage } from './types';

function App() {
  const [uploadData, setUploadData] = useState<UploadResponse | null>(null);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResponse | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisError, setAnalysisError] = useState<string | null>(null);
  
  // Conversational History
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  
  // Streaming states
  const [streamingLogs, setStreamingLogs] = useState<string[]>([]);
  const [partialCharts, setPartialCharts] = useState<ChartInfo[]>([]);
  const [partialStats, setPartialStats] = useState<StatisticsInfo | null>(null);

  const handleUploadSuccess = useCallback((data: UploadResponse) => {
    setUploadData(data);
    setAnalysisResult(null);
    setAnalysisError(null);
    setStreamingLogs([]);
    setPartialCharts([]);
    setPartialStats(null);
    setChatHistory([]);
  }, []);

  const handleQuery = useCallback(async (query: string) => {
    if (!uploadData) return;

    setIsAnalyzing(true);
    setAnalysisError(null);
    setAnalysisResult(null);
    setStreamingLogs([]);
    setPartialCharts([]);
    setPartialStats(null);

    let finalSummary = '';

    try {
      await analyzeQueryStream(
        uploadData.file_id,
        query,
        (event, data) => {
          if (event === 'status' || event === 'thought') {
            setStreamingLogs(prev => [...prev, data as string]);
          } else if (event === 'chart') {
            setPartialCharts(prev => [...prev, data as ChartInfo]);
          } else if (event === 'statistics') {
            setPartialStats(data as StatisticsInfo);
          } else if (event === 'final_result') {
            const result = data as AnalysisResponse;
            setAnalysisResult(result);
            finalSummary = result.summary;
          } else if (event === 'error') {
            const errorData = data as { detail?: string };
            setAnalysisError(errorData.detail || 'Analysis failed unexpectedly.');
          }
        },
        chatHistory
      );

      if (finalSummary) {
        setChatHistory(prev => [
          ...prev,
          { role: 'user', content: query },
          { role: 'assistant', content: finalSummary }
        ]);
      }
    } catch (err: any) {
      setAnalysisError(err.message || 'Connection to analysis stream failed.');
    } finally {
      setIsAnalyzing(false);
    }
  }, [uploadData, chatHistory]);

  return (
    <Layout>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '3rem' }}>
        {!uploadData ? (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', padding: '4rem 0' }}>
            <div style={{ padding: '0.4rem 1.2rem', background: 'var(--border-active)', color: 'var(--primary)', borderRadius: '100px', fontSize: '0.8rem', fontWeight: 700, marginBottom: '2rem', border: '1px solid var(--primary-glow)' }}>
              LUMINA ANALYST v1.0
            </div>
            <h1 className="text-gradient" style={{ fontSize: 'clamp(2.5rem, 8vw, 4.5rem)', lineHeight: 1.1, marginBottom: '1.5rem', maxWidth: '900px' }}>
              Transform Raw Data into <span style={{ color: 'var(--primary)', textShadow: '0 0 20px var(--primary-glow)' }}>Actionable Wisdom</span>
            </h1>
            <p style={{ fontSize: '1.25rem', color: 'var(--text-dim)', maxWidth: '700px', marginBottom: '4rem', lineHeight: 1.6 }}>
              Our multi-encrypted analytical engine processes complex datasets in real-time, delivering high-fidelity visualizations and deep neural synthesis.
            </p>
            <FileUpload onUploadSuccess={handleUploadSuccess} />
          </div>
        ) : (
          <div className="dashboard-grid animate-fade-in">
             {/* Sidebar Context */}
             <aside className="sidebar-context">
                <div className="glass-pane">
                   <h3 style={{ fontSize: '0.8rem', color: 'var(--primary)', textTransform: 'uppercase', letterSpacing: '0.15em', marginBottom: '1.5rem' }}>Active Context</h3>
                   <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
                         <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600 }}>Source File</span>
                         <span style={{ fontWeight: 700, fontSize: '1.1rem', wordBreak: 'break-all' }}>{uploadData.filename}</span>
                      </div>
                      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                         <div style={{ background: 'rgba(255,255,255,0.03)', padding: '1rem', borderRadius: '12px', border: '1px solid var(--border)' }}>
                            <div style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--primary)' }}>{uploadData.row_count.toLocaleString()}</div>
                            <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase' }}>Records</div>
                         </div>
                         <div style={{ background: 'rgba(255,255,255,0.03)', padding: '1rem', borderRadius: '12px', border: '1px solid var(--border)' }}>
                            <div style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--primary)' }}>{uploadData.column_count}</div>
                            <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase' }}>Dimensions</div>
                         </div>
                      </div>
                      <button 
                        onClick={() => setUploadData(null)}
                        style={{ width: '100%', marginTop: '1rem', padding: '0.75rem', background: 'transparent', border: '1px solid var(--border)', borderRadius: '12px', color: 'var(--text-dim)', fontWeight: 600, cursor: 'pointer' }}
                      >
                        Reset Environment
                      </button>
                   </div>
                </div>

                <div className="glass-pane">
                   <h3 style={{ fontSize: '0.8rem', color: 'var(--primary)', textTransform: 'uppercase', letterSpacing: '0.15em', marginBottom: '1.5rem' }}>Encryption Protocol</h3>
                   <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                         <span>Status</span>
                         <span style={{ color: 'var(--accent)', fontWeight: 700 }}>VERIFIED</span>
                      </div>
                      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                         <span>Algorithm</span>
                         <span>AES-256-GCM</span>
                      </div>
                   </div>
                </div>
             </aside>

             {/* Main Workspace */}
             <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
                <QueryInput
                  onSubmit={handleQuery}
                  isLoading={isAnalyzing}
                  disabled={!uploadData}
                />

                <ResultsPanel
                  result={analysisResult}
                  isLoading={isAnalyzing}
                  error={analysisError}
                  streamingLogs={streamingLogs}
                  partialCharts={partialCharts}
                  partialStats={partialStats}
                />

                <DataPreview data={uploadData} />
             </div>
          </div>
        )}
      </div>
    </Layout>
  );
}

export default App;
