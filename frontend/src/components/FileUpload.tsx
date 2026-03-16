import { useState, useRef, useCallback } from 'react';
import { Upload, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
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
      setError(err.message || 'Access Denied: Ingestion Failed');
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
    <div style={{ width: '100%', maxWidth: '700px', margin: '0 auto' }}>
      <div
        onDragOver={(e) => { e.preventDefault(); setIsDragOver(true); }}
        onDragLeave={() => setIsDragOver(false)}
        onDrop={onDrop}
        onClick={() => fileInputRef.current?.click()}
        style={{
          padding: 'clamp(2rem, 8vw, 4rem) clamp(1rem, 4vw, 2rem)',
          textAlign: 'center',
          cursor: 'pointer',
          transition: 'all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1)',
          background: isDragOver ? 'rgba(129, 140, 248, 0.08)' : 'var(--bg-card)',
          border: `2px dashed ${isDragOver ? 'var(--primary)' : 'var(--border)'}`,
          borderRadius: 'var(--radius-lg)',
          backdropFilter: 'var(--glass-blur)',
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
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1.5rem' }}>
            <Loader2 className="animate-spin" size={48} style={{ color: 'var(--primary)' }} />
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
              <span style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-main)' }}>Initializing Analytical Engine</span>
              <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Calibrating neural pathways...</span>
            </div>
          </div>
        ) : uploadedFile ? (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1rem' }}>
             <div style={{ width: '56px', height: '56px', background: 'rgba(45, 212, 191, 0.1)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--accent)', marginBottom: '0.5rem' }}>
               <CheckCircle size={28} />
             </div>
             <div style={{ marginBottom: '1rem' }}>
                <span style={{ fontSize: '1.2rem', fontWeight: 700, display: 'block' }}>Transmission Complete</span>
                <span style={{ color: 'var(--text-dim)', fontSize: '0.85rem' }}>Dataset indexed and ready</span>
             </div>
             <div className="glass-pane" style={{ background: 'rgba(255,255,255,0.02)', padding: '0.75rem 1rem', borderRadius: '12px', fontSize: '0.8rem', display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '0.5rem' }}>
               <strong style={{ color: 'var(--primary)', wordBreak: 'break-all' }}>{uploadedFile.filename}</strong>
               <span className="file-meta-separator">|</span>
               <span>{uploadedFile.row_count.toLocaleString()} Records</span>
               <span className="file-meta-separator">|</span>
               <span>{formatSize(uploadedFile.file_size)}</span>
             </div>
          </div>
        ) : (
          <div>
            <div style={{ width: '64px', height: '64px', margin: '0 auto 1.5rem', background: 'rgba(129, 140, 248, 0.05)', borderRadius: '20px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--primary)', position: 'relative' }}>
              <Upload size={28} />
              <div style={{ position: 'absolute', inset: 0, border: '1px solid var(--primary-glow)', borderRadius: '20px' }} className="animate-pulse" />
            </div>
            <h3 style={{ fontSize: 'clamp(1.2rem, 5vw, 1.5rem)', marginBottom: '0.75rem' }} className="text-gradient">Inject Knowledge Source</h3>
            <p style={{ color: 'var(--text-dim)', maxWidth: '400px', margin: '0 auto 1.5rem', fontSize: '0.95rem' }}>Drop your dataset here to empower the agent with secure, local intelligence.</p>
            <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.1em' }}>
              Maximum Security Protocol Enabled
            </div>
          </div>
        )}
      </div>

      {error && (
        <div style={{ marginTop: '1.5rem', padding: '1rem 1.5rem', background: 'rgba(244, 114, 182, 0.08)', borderRadius: '12px', border: '1px solid rgba(244, 114, 182, 0.2)', display: 'flex', alignItems: 'center', gap: '1rem', color: 'var(--text-main)' }} className="animate-fade-in">
          <AlertCircle style={{ color: '#f472b6' }} />
          <span>{error}</span>
        </div>
      )}
    </div>
  );
}
