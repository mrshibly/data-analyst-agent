import { useState, useCallback, useRef, useEffect } from 'react';
import Layout from './components/Layout';
import FileUpload from './components/FileUpload';
import QueryInput from './components/QueryInput';
import ResultsPanel from './components/ResultsPanel';
import DataDrawer from './components/DataDrawer';
import { analyzeQueryStream } from './services/api';
import type { UploadResponse, AnalysisResponse, ChartInfo, StatisticsInfo, ChatMessage } from './types';

interface ConversationTurn {
  id: string;
  query: string;
  result: AnalysisResponse | null;
  isLoading: boolean;
  error: string | null;
  streamingLogs: string[];
  partialCharts: ChartInfo[];
  partialStats: StatisticsInfo | null;
}

function App() {
  const [uploadData, setUploadData] = useState<UploadResponse | null>(null);
  const [turns, setTurns] = useState<ConversationTurn[]>([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);

  // Conversational History for LLM backend
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const chatBottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [turns]);

  const handleUploadSuccess = useCallback((data: UploadResponse) => {
    setUploadData(data);
    setTurns([]);
    setChatHistory([]);
  }, []);

  const handleQuery = useCallback(async (query: string) => {
    if (!uploadData) return;

    const turnId = Date.now().toString();
    const newTurn: ConversationTurn = {
      id: turnId,
      query,
      result: null,
      isLoading: true,
      error: null,
      streamingLogs: [],
      partialCharts: [],
      partialStats: null,
    };

    setTurns(prev => [...prev, newTurn]);
    setIsAnalyzing(true);

    let finalSummary = '';

    try {
      await analyzeQueryStream(
        uploadData.file_id,
        query,
        (event, data) => {
          setTurns(prev => prev.map(t => {
            if (t.id !== turnId) return t;

            if (event === 'status' || event === 'thought') {
              return { ...t, streamingLogs: [...t.streamingLogs, data as string] };
            } else if (event === 'chart') {
              return { ...t, partialCharts: [...t.partialCharts, data as ChartInfo] };
            } else if (event === 'statistics') {
              return { ...t, partialStats: data as StatisticsInfo };
            } else if (event === 'final_result') {
              const res = data as AnalysisResponse;
              finalSummary = res.summary;
              return { ...t, result: res, isLoading: false };
            } else if (event === 'error') {
              const err = data as { detail?: string };
              return { ...t, error: err.detail || 'Analysis failed.', isLoading: false };
            }
            return t;
          }));
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
      setTurns(prev => prev.map(t => t.id === turnId ? { ...t, error: err.message || 'Stream connection failed.', isLoading: false } : t));
    } finally {
      setIsAnalyzing(false);
    }
  }, [uploadData, chatHistory]);

  const handleExportReport = () => {
    if (!uploadData || turns.length === 0) return;
    
    const dateStr = new Date().toLocaleDateString('en-US', { dateStyle: 'full' });
    let htmlContent = `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Lumina Analyst Executive Report - ${uploadData.filename}</title>
  <style>
    body { font-family: 'Segoe UI', system-ui, sans-serif; margin: 40px; color: #1e293b; background: #f8fafc; }
    .header { border-bottom: 3px solid #6366f1; padding-bottom: 20px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: flex-end; }
    .brand { font-size: 24px; font-weight: 800; color: #4f46e5; }
    .meta { font-size: 14px; color: #64748b; }
    .kpi-row { display: flex; gap: 20px; margin-bottom: 30px; }
    .kpi-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 15px 25px; flex: 1; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
    .kpi-value { font-size: 28px; font-weight: 800; color: #6366f1; }
    .kpi-label { font-size: 12px; font-weight: 700; color: #94a3b8; text-transform: uppercase; }
    .section { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 25px; margin-bottom: 25px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
    .query-title { font-size: 18px; font-weight: 700; color: #0f172a; margin-bottom: 12px; border-left: 4px solid #6366f1; padding-left: 12px; }
    .summary-text { font-size: 15px; line-height: 1.6; color: #334155; margin-bottom: 15px; }
    .insight-bullet { background: #f1f5f9; padding: 10px 15px; border-radius: 8px; margin-bottom: 8px; font-size: 14px; color: #1e293b; }
    @media print { body { margin: 0; background: #fff; } .section { page-break-inside: avoid; } }
  </style>
</head>
<body>
  <div class="header">
    <div>
      <div class="brand">💎 Lumina Analyst</div>
      <div style="font-size: 14px; color: #64748b; margin-top: 4px;">Executive Data Intelligence Report</div>
    </div>
    <div class="meta">
      <div><strong>Dataset:</strong> ${uploadData.filename}</div>
      <div><strong>Date:</strong> ${dateStr}</div>
    </div>
  </div>

  <div class="kpi-row">
    <div class="kpi-card">
      <div class="kpi-value">${uploadData.row_count.toLocaleString()}</div>
      <div class="kpi-label">Total Records</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-value">${uploadData.column_count}</div>
      <div class="kpi-label">Attributes</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-value">${turns.length}</div>
      <div class="kpi-label">Analytical Queries</div>
    </div>
  </div>
`;

    turns.forEach((t, i) => {
      if (t.result) {
        htmlContent += `
  <div class="section">
    <div class="query-title">Query ${i + 1}: ${t.query}</div>
    <div class="summary-text">${t.result.summary}</div>
    ${t.result.insights && t.result.insights.length > 0 ? `
      <div style="font-weight: 700; font-size: 13px; color: #64748b; text-transform: uppercase; margin-bottom: 10px;">Key Insights</div>
      ${t.result.insights.map(ins => `<div class="insight-bullet">• ${ins}</div>`).join('')}
    ` : ''}
  </div>`;
      }
    });

    htmlContent += `
</body>
</html>`;

    const printWindow = window.open('', '_blank');
    if (printWindow) {
      printWindow.document.write(htmlContent);
      printWindow.document.close();
      setTimeout(() => printWindow.print(), 500);
    }
  };

  return (
    <Layout 
      activeData={uploadData}
      onOpenDrawer={() => setIsDrawerOpen(true)}
      onResetData={() => setUploadData(null)}
      onExportReport={turns.length > 0 ? handleExportReport : undefined}
    >
      <DataDrawer 
        data={uploadData} 
        isOpen={isDrawerOpen} 
        onClose={() => setIsDrawerOpen(false)} 
      />

      {!uploadData ? (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', padding: '4rem 1rem' }}>
          <h1 className="text-gradient" style={{ fontSize: 'clamp(2.4rem, 6vw, 4rem)', lineHeight: 1.15, marginBottom: '1.25rem', maxWidth: '880px', fontWeight: 800 }}>
            Transform Complex Data into <span style={{ color: 'var(--primary)', textShadow: '0 0 30px var(--primary-glow)' }}>Executive Intelligence</span>
          </h1>
          <p style={{ fontSize: '1.15rem', color: 'var(--text-dim)', maxWidth: '680px', marginBottom: '3.5rem', lineHeight: 1.6 }}>
            Autonomous analytical engine powered by LLMs, instant SQL aggregation, and dynamic interactive visual insights.
          </p>
          <FileUpload onUploadSuccess={handleUploadSuccess} />
        </div>
      ) : (
        <div className="chat-container">
          {turns.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '3rem 1rem', color: 'var(--text-dim)' }}>
              <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-main)', marginBottom: '0.5rem' }}>
                Dataset Loaded: <span style={{ color: 'var(--accent-cyan)' }}>{uploadData.filename}</span>
              </h2>
              <p style={{ fontSize: '0.95rem', color: 'var(--text-muted)' }}>
                Ask a question using the prompt bar below to start the conversational data analysis session.
              </p>
            </div>
          ) : (
            turns.map((turn) => (
              <div key={turn.id} className="message-turn">
                {/* User Message Bubble */}
                <div className="user-message-bubble">
                  {turn.query}
                </div>

                {/* Assistant Response Card */}
                <ResultsPanel 
                  result={turn.result}
                  isLoading={turn.isLoading}
                  error={turn.error}
                  streamingLogs={turn.streamingLogs}
                  partialCharts={turn.partialCharts}
                  partialStats={turn.partialStats}
                />
              </div>
            ))
          )}

          <div ref={chatBottomRef} />
        </div>
      )}

      {/* Floating Sticky Command Bar */}
      <QueryInput
        onSubmit={handleQuery}
        isLoading={isAnalyzing}
        disabled={!uploadData}
      />
    </Layout>
  );
}

export default App;
