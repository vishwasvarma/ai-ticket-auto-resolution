import React from 'react';

const statusColors = {
  Open: '#fde047', // Yellow
  Resolved: '#22c55e', // Green
  'Needs Attention': '#ef4444', // Red
};

const StatusBadge = ({ status }) => (
  <span style={{
    background: statusColors[status] || '#64748b',
    color: '#0f172a',
    borderRadius: 8,
    padding: '4px 12px',
    fontWeight: 600,
    fontSize: 13,
    marginLeft: 8,
  }}>
    {status}
  </span>
);

export default StatusBadge;
