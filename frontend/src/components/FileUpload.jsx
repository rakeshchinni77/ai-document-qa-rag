import React, { useState, useRef } from 'react';
import { Upload, FileText, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import { uploadDocument } from '../services/api';

export default function FileUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [statusMsg, setStatusMsg] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef(null);

  const allowedExtensions = ['.txt', '.md', '.pdf'];

  const validateFile = (selectedFile) => {
    if (!selectedFile) return false;
    const ext = selectedFile.name.substring(selectedFile.name.lastIndexOf('.')).toLowerCase();
    if (!allowedExtensions.includes(ext)) {
      setErrorMsg(`Unsupported file format. Please upload .txt, .md, or .pdf`);
      setFile(null);
      return false;
    }
    setErrorMsg(null);
    return true;
  };

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (validateFile(selected)) {
      setFile(selected);
      setStatusMsg(null);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    const droppedFile = e.dataTransfer.files[0];
    if (validateFile(droppedFile)) {
      setFile(droppedFile);
      setStatusMsg(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    setErrorMsg(null);
    setStatusMsg(null);

    try {
      const res = await uploadDocument(file);
      setStatusMsg(`File uploaded and indexed successfully (${res.chunks_indexed} chunks)`);
      setFile(null);
      if (fileInputRef.current) fileInputRef.current.value = '';
      if (onUploadSuccess) onUploadSuccess(res);
    } catch (err) {
      setErrorMsg(err.message || 'Failed to upload document.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="glass-panel" style={{ padding: '1.5rem', marginBottom: '1.5rem' }}>
      <h2 style={{ fontSize: '1rem', fontWeight: 800, letterSpacing: '0.05em', color: 'var(--text-muted)', marginBottom: '1rem', textTransform: 'uppercase' }}>
        DOCUMENT INGESTION
      </h2>

      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        style={{
          border: `2px dashed ${isDragOver ? 'var(--accent-primary)' : 'var(--border-color)'}`,
          borderRadius: 'var(--radius-md)',
          padding: '2rem 1rem',
          textAlign: 'center',
          cursor: 'pointer',
          background: isDragOver ? 'rgba(99, 102, 241, 0.08)' : 'rgba(10, 13, 20, 0.4)',
          transition: 'all 0.2s ease',
          marginBottom: '1rem'
        }}
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept=".txt,.md,.pdf"
          style={{ display: 'none' }}
        />
        <FileText size={32} style={{ color: 'var(--accent-cyan)', marginBottom: '0.5rem' }} />
        <p style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-primary)' }}>
          {file ? file.name : 'Drop PDF / TXT / MD here'}
        </p>
        <div style={{ marginTop: '0.5rem' }}>
          <span className="btn btn-secondary" style={{ fontSize: '0.8rem', padding: '0.35rem 0.85rem' }}>
            Choose Document
          </span>
        </div>
      </div>

      {errorMsg && (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          background: 'rgba(244, 63, 94, 0.1)',
          border: '1px solid rgba(244, 63, 94, 0.3)',
          padding: '0.75rem',
          borderRadius: 'var(--radius-sm)',
          color: '#fda4af',
          fontSize: '0.85rem',
          marginBottom: '1rem'
        }}>
          <AlertCircle size={16} />
          <span>{errorMsg}</span>
        </div>
      )}

      {statusMsg && (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          background: 'rgba(16, 185, 129, 0.1)',
          border: '1px solid rgba(16, 185, 129, 0.3)',
          padding: '0.75rem',
          borderRadius: 'var(--radius-sm)',
          color: '#6ee7b7',
          fontSize: '0.85rem',
          marginBottom: '1rem'
        }}>
          <CheckCircle size={16} />
          <span>{statusMsg}</span>
        </div>
      )}

      <button
        onClick={handleUpload}
        disabled={!file || uploading}
        className="btn btn-primary"
        style={{ width: '100%', opacity: (!file || uploading) ? 0.6 : 1 }}
      >
        {uploading ? (
          <>
            <Loader2 className="spinner" size={18} />
            <span>Indexing Document...</span>
          </>
        ) : (
          <>
            <Upload size={18} />
            <span>Upload & Index</span>
          </>
        )}
      </button>
    </div>
  );
}
