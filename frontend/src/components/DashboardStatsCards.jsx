import React from 'react';

const cardColors = {
  total: '#3b82f6',
  resolved: '#22c55e',
  open: '#fde047',
  attention: '#ef4444',
};

const DashboardStatsCards = ({ stats }) => (
  <div style={{ display: 'flex', gap: 20, marginBottom: 24 }}>
    <div style={{ background: cardColors.total, color: '#0f172a', borderRadius: 10, padding: 18, minWidth: 120, textAlign: 'center', fontWeight: 600 }}>
      Total<br />{stats.total}
    </div>
    <div style={{ background: cardColors.resolved, color: '#0f172a', borderRadius: 10, padding: 18, minWidth: 120, textAlign: 'center', fontWeight: 600 }}>
      Resolved<br />{stats.resolved}
    </div>
    <div style={{ background: cardColors.open, color: '#0f172a', borderRadius: 10, padding: 18, minWidth: 120, textAlign: 'center', fontWeight: 600 }}>
      Open<br />{stats.open}
    </div>
    <div style={{ background: cardColors.attention, color: '#0f172a', borderRadius: 10, padding: 18, minWidth: 120, textAlign: 'center', fontWeight: 600 }}>
      Needs Attention<br />{stats.attention}
    </div>
  </div>
);

export default DashboardStatsCards;
