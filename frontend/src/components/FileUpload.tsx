import { useState, useRef, useCallback } from 'react';
import { Upload, CheckCircle2, AlertTriangle, Loader2, FileSpreadsheet, Sparkles } from 'lucide-react';
import { uploadFile } from '../services/api';
import type { UploadResponse } from '../types';

interface FileUploadProps {
  onUploadSuccess: (data: UploadResponse) => void;
}

export default function FileUpload({ onUploadSuccess }: FileUploadProps) {
  const [isDragOver, setIsDragOver] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [uploadedFile, setUploadedFile] = useState<UploadResponse | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFile = useCallback(async (file: File) => {
    setError(null);
    setIsUploading(true);
    setUploadedFile(null);

    try {
      const result = await uploadFile(file);
      setUploadedFile(result);
      onUploadSuccess(result);
    } catch (err: any) {
      setError(err.message || 'Dataset Ingestion Failed');
    } finally {
      setIsUploading(false);
    }
  }, [onUploadSuccess]);

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  };

  const formatSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1048576) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / 1048576).toFixed(1)} MB`;
  };

  return (
    <div style={{ width: '100%', maxWidth: '720px', margin: '0 auto' }}>
      <div
        onDragOver={(e) => { e.preventDefault(); setIsDragOver(true); }}
        onDragLeave={() => setIsDragOver(false)}
        onDrop={onDrop}
        onClick={() => fileInputRef.current?.click()}
        style={{
          padding: 'clamp(2.5rem, 6vw, 4rem) clamp(1.5rem, 4vw, 3rem)',
          textAlign: 'center',
          cursor: 'pointer',
          transition: 'all 0.35s cubic-bezier(0.16, 1, 0.3, 1)',
          background: isDragOver ? 'rgba(99, 102, 241, 0.12)' : 'var(--bg-card)',
          border: `2px dashed ${isDragOver ? 'var(--accent-cyan)' : 'rgba(99, 102, 241, 0.3)'}`,
          borderRadius: 'var(--radius-xl)',
          backdropFilter: 'var(--glass-blur)',
          boxShadow: isDragOver ? '0 20px 50px rgba(99, 102, 241, 0.25)' : '0 12px 40px rgba(0, 0, 0, 0.4)',
          position: 'relative',
          overflow: 'hidden'
        }}
        className="animate-fade-in"
      >
        <input 
          type="file" 
          ref={fileInputRef} 
          hidden 
          accept=".csv,.xlsx,.xls" 
          onChange={(e) => { const file = e.target.files?.[0]; if (file) handleFile(file); }}
        />

        {isUploading ? (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1.5rem', padding: '1rem 0' }}>
            <div style={{ position: 'relative', width: '64px', height: '64px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Loader2 className="animate-spin" size={48} style={{ color: 'var(--primary)' }} />
              <Sparkles size={20} style={{ position: 'absolute', color: 'var(--accent-cyan)' }} />
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
              <span style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--text-main)' }}>Initializing Dataset Indexer</span>
              <span style={{ fontSize: '0.85rem', color: 'var(--accent-cyan)', fontWeight: 600 }}>Parsing schema & computing descriptive metrics...</span>
            </div>
          </div>
        ) : uploadedFile ? (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1.25rem' }}>
             <div style={{ width: '64px', height: '64px', background: 'rgba(16, 185, 129, 0.12)', border: '1px solid rgba(16, 185, 129, 0.3)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--accent-emerald)' }}>
               <CheckCircle2 size={32} />
             </div>
             <div>
                <span style={{ fontSize: '1.3rem', fontWeight: 800, display: 'block', marginBottom: '0.25rem' }}>Ingestion Complete</span>
                <span style={{ color: 'var(--text-dim)', fontSize: '0.9rem' }}>Dataset structured and synchronized with AI engine</span>
             </div>
             <div 
               style={{ 
                 background: 'rgba(255, 255, 255, 0.03)', 
                 border: '1px solid var(--border)', 
                 padding: '0.85rem 1.25rem', 
                 borderRadius: 'var(--radius-md)', 
                 fontSize: '0.85rem', 
                 display: 'flex', 
                 alignItems: 'center',
                 gap: '1rem',
                 marginTop: '0.5rem'
               }}
             >
               <FileSpreadsheet size={20} style={{ color: 'var(--primary)' }} />
               <strong style={{ color: 'var(--text-main)', wordBreak: 'break-all' }}>{uploadedFile.filename}</strong>
               <span style={{ color: 'var(--text-muted)' }}>•</span>
               <span style={{ color: 'var(--accent-cyan)', fontWeight: 700 }}>{uploadedFile.row_count.toLocaleString()} rows</span>
               <span style={{ color: 'var(--text-muted)' }}>•</span>
               <span style={{ color: 'var(--text-dim)' }}>{formatSize(uploadedFile.file_size)}</span>
             </div>
          </div>
        ) : (
          <div>
            <div style={{ 
              width: '72px', 
              height: '72px', 
              margin: '0 auto 1.75rem', 
              background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(6, 182, 212, 0.15))', 
              border: '1px solid rgba(99, 102, 241, 0.3)',
              borderRadius: '24px', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center', 
              color: 'var(--primary)', 
              position: 'relative' 
            }}>
              <Upload size={32} />
            </div>

            <h3 style={{ fontSize: 'clamp(1.3rem, 4vw, 1.6rem)', marginBottom: '0.75rem' }} className="text-gradient">
              Upload Dataset for Analysis
            </h3>
            <p style={{ color: 'var(--text-dim)', maxWidth: '440px', margin: '0 auto 1.75rem', fontSize: '0.95rem', lineHeight: 1.6 }}>
              Drag & drop your CSV or Excel file here to begin real-time streaming analytics and interactive charts.
            </p>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem', padding: '0.4rem 1rem', background: 'rgba(255, 255, 255, 0.03)', border: '1px solid var(--border)', borderRadius: '100px', fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600 }}>
              <Sparkles size={14} style={{ color: 'var(--accent-cyan)' }} />
              Supported formats: .CSV, .XLSX, .XLS (Up to 50MB)
            </div>
          </div>
        )}
      </div>

      {error && (
        <div style={{ marginTop: '1.5rem', padding: '1rem 1.5rem', background: 'rgba(236, 72, 153, 0.1)', borderRadius: 'var(--radius-md)', border: '1px solid rgba(236, 72, 153, 0.3)', display: 'flex', alignItems: 'center', gap: '1rem', color: '#fbcfe8' }} className="animate-fade-in">
          <AlertTriangle style={{ color: 'var(--accent-pink)' }} />
          <span>{error}</span>
        </div>
      )}
    </div>
  );
}
