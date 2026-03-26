import React, { useState } from 'react';
import StatusBadge from './StatusBadge';

const TicketCard = ({ ticket, onExpand }) => {
  const [expanded, setExpanded] = useState(false);
  const handleExpand = () => {
    setExpanded(!expanded);
    if (onExpand) onExpand(ticket);
  };
  return (
    <div className="ticket-card" style={{ background: '#1f2933', color: '#e5e7eb', borderRadius: 12, marginBottom: 16, padding: 20, boxShadow: '0 2px 8px #0f172a33' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <div style={{ fontWeight: 600, fontSize: 18 }}>{ticket.title}</div>
          <div style={{ fontSize: 14, color: '#94a3b8' }}>#{ticket.ticket_number} • {ticket.category} • Confidence: {(ticket.confidence * 100).toFixed(1)}%</div>
        </div>
        <StatusBadge status={ticket.status} />
      </div>
      <div style={{ marginTop: 12 }}>
        <div style={{ fontSize: 15 }}>{ticket.description}</div>
        {expanded && (
          <div style={{ marginTop: 10, background: '#111827', padding: 12, borderRadius: 8 }}>
            <div><b>AI Response:</b> {ticket.ai_response}</div>
            <div style={{ marginTop: 6, fontSize: 13, color: '#60a5fa' }}>Created: {new Date(ticket.created_at).toLocaleString()}</div>
          </div>
        )}
      </div>
      <button onClick={handleExpand} style={{ marginTop: 10, background: '#3b82f6', color: '#e5e7eb', border: 'none', borderRadius: 6, padding: '6px 16px', cursor: 'pointer', fontWeight: 500 }}>
        {expanded ? 'Hide Details' : 'Show Details'}
      </button>
    </div>
  );
};

export default TicketCard;
