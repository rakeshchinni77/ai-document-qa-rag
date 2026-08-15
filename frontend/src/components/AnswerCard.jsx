import React, { useState } from 'react';
import { Copy, Check } from 'lucide-react';

export default function AnswerCard({ answer, loading }) {
  const [copied, setCopied] = useState(false);

  if (!answer && !loading) return null;

  const handleCopy = () => {
    if (!answer) return;
    navigator.clipboard.writeText(answer);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="glass-panel" style={{ padding: '1.5rem', marginBottom: '1.5rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
        <h3 style={{ fontSize: '1rem', fontWeight: 800, letterSpacing: '0.05em', color: 'var(--text-muted)', textTransform: 'uppercase' }}>
          ANSWER
        </h3>
        {answer && (
          <button onClick={handleCopy} className="btn btn-secondary" style={{ padding: '0.3rem 0.75rem', fontSize: '0.78rem' }}>
            {copied ? <Check size={14} style={{ color: '#34d399' }} /> : <Copy size={14} />}
            <span>{copied ? 'Copied' : 'Copy'}</span>
          </button>
        )}
      </div>

      <hr style={{ borderColor: 'var(--border-color)', marginBottom: '1rem', opacity: 0.5 }} />

      {loading ? (
        <div style={{ padding: '0.5rem 0' }}>
          <div className="pulsing" style={{ height: '14px', background: 'rgba(255,255,255,0.1)', borderRadius: '4px', marginBottom: '8px', width: '90%' }}></div>
          <div className="pulsing" style={{ height: '14px', background: 'rgba(255,255,255,0.1)', borderRadius: '4px', marginBottom: '8px', width: '95%' }}></div>
          <div className="pulsing" style={{ height: '14px', background: 'rgba(255,255,255,0.1)', borderRadius: '4px', width: '70%' }}></div>
        </div>
      ) : (
        <div style={{ color: '#f8fafc', fontSize: '0.98rem', lineHeight: '1.7', whiteSpace: 'pre-wrap' }}>
          {answer}
        </div>
      )}
    </div>
  );
}
