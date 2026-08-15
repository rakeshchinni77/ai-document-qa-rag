import React, { useState } from 'react';
import { Send, Loader2 } from 'lucide-react';

export default function QuestionInput({ onQuerySubmit, loading }) {
  const [question, setQuestion] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!question.trim() || loading) return;
    onQuerySubmit(question.trim());
  };

  return (
    <div className="glass-panel" style={{ padding: '1.5rem', marginBottom: '1.5rem' }}>
      <h2 style={{ fontSize: '1rem', fontWeight: 800, letterSpacing: '0.05em', color: 'var(--text-muted)', marginBottom: '1rem', textTransform: 'uppercase' }}>
        ASK YOUR DOCUMENT
      </h2>

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '1rem' }}>
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="What is the main conclusion?"
            className="form-input"
            disabled={loading}
            style={{ fontSize: '1rem', padding: '0.9rem 1.25rem' }}
          />
        </div>

        <button
          type="submit"
          disabled={!question.trim() || loading}
          className="btn btn-primary"
          style={{ width: '100%', opacity: (!question.trim() || loading) ? 0.6 : 1 }}
        >
          {loading ? (
            <>
              <Loader2 className="spinner" size={18} />
              <span>Generating Answer...</span>
            </>
          ) : (
            <>
              <Send size={18} />
              <span>Ask</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
}
