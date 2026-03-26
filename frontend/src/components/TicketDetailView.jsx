import React from 'react';
import StatusBadge from './StatusBadge';

const TicketDetailView = ({ ticket, onClose }) => {
  if (!ticket) return null;
  return (
    <div style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', background: '#0f172aee', zIndex: 1000, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
      <div style={{ background: '#1f2933', color: '#e5e7eb', borderRadius: 14, padding: 32, minWidth: 340, maxWidth: 480, boxShadow: '0 4px 24px #0f172a88', position: 'relative' }}>
        <button onClick={onClose} style={{ position: 'absolute', top: 12, right: 12, background: 'none', border: 'none', color: '#e5e7eb', fontSize: 22, cursor: 'pointer' }}>&times;</button>
        <div style={{ fontWeight: 700, fontSize: 22, marginBottom: 8 }}>{ticket.title}</div>
        <div style={{ fontSize: 15, color: '#94a3b8', marginBottom: 8 }}>#{ticket.ticket_number} • {ticket.category} • Confidence: {(ticket.confidence * 100).toFixed(1)}%</div>
        <StatusBadge status={ticket.status} />
        <div style={{ marginTop: 18, fontSize: 16 }}>{ticket.description}</div>
        <div style={{ marginTop: 18, background: '#111827', padding: 14, borderRadius: 8 }}>
          <b>AI Response:</b> {ticket.ai_response}
        </div>
        <div style={{ marginTop: 10, fontSize: 13, color: '#60a5fa' }}>Created: {new Date(ticket.created_at).toLocaleString()}</div>
      </div>
    </div>
  );
};

export default TicketDetailView;
