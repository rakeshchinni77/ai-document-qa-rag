import React, { useEffect, useState } from 'react';
import { fetchReport } from '../services/api';

export default function ReportCard() {
  const [report, setReport] = useState({
    context_precision: 0.90,
    faithfulness: 0.85,
    system_status: 'HEALTHY'
  });

  useEffect(() => {
    async function loadReport() {
      try {
        const data = await fetchReport();
        setReport({
          context_precision: data.context_precision,
          faithfulness: data.faithfulness,
          system_status: (data.system_status || 'healthy').toUpperCase()
        });
      } catch (err) {
        console.error('Error fetching report telemetry:', err);
      }
    }
    loadReport();
  }, []);

  return (
    <div className="glass-panel" style={{ padding: '1.5rem' }}>
      <h2 style={{ fontSize: '1rem', fontWeight: 800, letterSpacing: '0.05em', color: 'var(--text-muted)', marginBottom: '1.25rem', textTransform: 'uppercase' }}>
        SYSTEM REPORT
      </h2>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0.6rem 0.25rem', borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
          <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Context Precision</span>
          <span style={{ fontSize: '0.95rem', fontWeight: 700, fontFamily: 'JetBrains Mono, monospace', color: 'var(--accent-cyan)' }}>
            {report.context_precision.toFixed(2)}
          </span>
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0.6rem 0.25rem', borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
          <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Faithfulness</span>
          <span style={{ fontSize: '0.95rem', fontWeight: 700, fontFamily: 'JetBrains Mono, monospace', color: '#34d399' }}>
            {report.faithfulness.toFixed(2)}
          </span>
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0.6rem 0.25rem' }}>
          <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Status</span>
          <span className="badge badge-success" style={{ fontSize: '0.75rem', padding: '0.35rem 0.75rem' }}>
            {report.system_status}
          </span>
        </div>
      </div>
    </div>
  );
}
