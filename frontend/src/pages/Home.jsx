import React, { useState, useEffect } from 'react';
import FileUpload from '../components/FileUpload';
import QuestionInput from '../components/QuestionInput';
import AnswerCard from '../components/AnswerCard';
import SourceCard from '../components/SourceCard';
import ReportCard from '../components/ReportCard';
import { queryDocument, fetchDocuments } from '../services/api';
import { Sparkles, AlertCircle } from 'lucide-react';

export default function Home() {
  const [queryAnswer, setQueryAnswer] = useState(null);
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [docSummary, setDocSummary] = useState({ documents: [], total_chunks: 0 });

  const loadDocumentSummary = async () => {
    try {
      const summary = await fetchDocuments();
      setDocSummary(summary);
    } catch (err) {
      console.error('Failed to load document summary:', err);
    }
  };

  useEffect(() => {
    loadDocumentSummary();
  }, []);

  const handleQuerySubmit = async (question) => {
    setLoading(true);
    setError(null);
    setQueryAnswer(null);
    setSources([]);

    try {
      const res = await queryDocument(question);
      setQueryAnswer(res.answer);
      setSources(res.sources || []);
    } catch (err) {
      setError(err.message || 'An error occurred while answering your query.');
    } finally {
      setLoading(false);
    }
  };

  const handleUploadSuccess = () => {
    loadDocumentSummary();
  };

  return (
    <div style={{ maxWidth: '780px', margin: '0 auto', padding: '2rem 1rem' }}>
      {/* Header Title Frame */}
      <header className="glass-panel" style={{ padding: '1.75rem', textAlign: 'center', marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '1.6rem', fontWeight: 900, letterSpacing: '0.08em', color: '#f8fafc', marginBottom: '0.35rem' }}>
          AI DOCUMENT INTELLIGENCE
        </h1>
        <p style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--accent-cyan)', letterSpacing: '0.02em' }}>
          RAG Question Answering System
        </p>
      </header>

      {/* 1. DOCUMENT INGESTION SECTION */}
      <FileUpload onUploadSuccess={handleUploadSuccess} />

      {/* 2. ASK YOUR DOCUMENT SECTION */}
      <QuestionInput onQuerySubmit={handleQuerySubmit} loading={loading} />

      {error && (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.75rem',
          background: 'rgba(244, 63, 94, 0.1)',
          border: '1px solid rgba(244, 63, 94, 0.3)',
          padding: '1rem',
          borderRadius: 'var(--radius-md)',
          color: '#fda4af',
          marginBottom: '1.5rem'
        }}>
          <AlertCircle size={20} />
          <div>
            <p style={{ fontWeight: 600, fontSize: '0.9rem' }}>Query Error</p>
            <p style={{ fontSize: '0.85rem', opacity: 0.9 }}>{error}</p>
          </div>
        </div>
      )}

      {/* ANSWER SECTION */}
      <AnswerCard answer={queryAnswer} loading={loading} />

      {/* SOURCES SECTION */}
      <SourceCard sources={sources} />

      {/* 3. SYSTEM REPORT SECTION */}
      <ReportCard />
    </div>
  );
}
