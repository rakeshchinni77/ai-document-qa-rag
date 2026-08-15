import React from 'react';

export default function SourceCard({ sources }) {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="glass-panel" style={{ padding: '1.5rem', marginBottom: '1.5rem' }}>
      <h3 style={{ fontSize: '1rem', fontWeight: 800, letterSpacing: '0.05em', color: 'var(--text-muted)', marginBottom: '0.5rem', textTransform: 'uppercase' }}>
        SOURCES
      </h3>

      <hr style={{ borderColor: 'var(--border-color)', marginBottom: '1rem', opacity: 0.5 }} />

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {sources.map((source, idx) => (
          <div
            key={idx}
            style={{
              background: 'rgba(10, 13, 20, 0.6)',
              border: '1px solid var(--border-color)',
              borderRadius: 'var(--radius-md)',
              padding: '1rem'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
              <span style={{ fontSize: '1rem' }}>📄</span>
              <span style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--accent-cyan)' }}>
                Document Chunk #{idx + 1}
              </span>
            </div>

            <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', fontFamily: 'JetBrains Mono, monospace', lineHeight: '1.5', whiteSpace: 'pre-wrap' }}>
              "{source}"
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
