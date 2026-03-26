import { useEffect, useState } from "react";
import API from "../services/api";
import StatusBadge from "../components/StatusBadge";
import LoadingSpinner from "../components/LoadingSpinner";
import DashboardStatsCards from "../components/DashboardStatsCards";
import TicketDetailView from "../components/TicketDetailView";

const statusOptions = ["All", "Open", "Resolved", "Needs Attention"];

export default function AdminDashboard({ user }) {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [statusFilter, setStatusFilter] = useState("All");
  const [search, setSearch] = useState("");
  const [sortBy, setSortBy] = useState("created_at");
  const [sortDir, setSortDir] = useState("desc");
  const [selectedTicket, setSelectedTicket] = useState(null);

  const fetchTickets = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await API.get("/tickets", {
        headers: { user_id: user.user_id },
      });
      setTickets(res.data);
    } catch (err) {
      setError("Failed to fetch tickets");
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchTickets();
    // eslint-disable-next-line
  }, []);

  // Stats
  const stats = {
    total: tickets.length,
    resolved: tickets.filter(t => t.status === "Resolved").length,
    open: tickets.filter(t => t.status === "Open").length,
    attention: tickets.filter(t => t.status === "Needs Attention").length,
  };

  // Filter, search, sort
  let filtered = tickets;
  if (statusFilter !== "All") filtered = filtered.filter(t => t.status === statusFilter);
  if (search) filtered = filtered.filter(t => (
    t.title.toLowerCase().includes(search.toLowerCase()) ||
    t.ticket_number.toString().includes(search) ||
    t.category?.toLowerCase().includes(search.toLowerCase())
  ));
  filtered = filtered.sort((a, b) => {
    if (sortBy === "created_at") {
      return sortDir === "desc"
        ? new Date(b.created_at) - new Date(a.created_at)
        : new Date(a.created_at) - new Date(b.created_at);
    }
    if (sortBy === "status") {
      return sortDir === "desc"
        ? b.status.localeCompare(a.status)
        : a.status.localeCompare(b.status);
    }
    return 0;
  });

  return (
    <div style={{ background: '#0f172a', minHeight: '100vh', color: '#e5e7eb', padding: 0 }}>
      <div style={{ maxWidth: 1100, margin: '0 auto', padding: 24 }}>
        <h2 style={{ fontWeight: 700, fontSize: 28, marginBottom: 10 }}>Admin Dashboard</h2>
        <DashboardStatsCards stats={stats} />

        <div style={{ display: 'flex', gap: 16, marginBottom: 18, flexWrap: 'wrap' }}>
          <select value={statusFilter} onChange={e => setStatusFilter(e.target.value)} style={{ background: '#1f2933', color: '#e5e7eb', border: 'none', borderRadius: 6, padding: 8, fontSize: 15 }}>
            {statusOptions.map(opt => <option key={opt}>{opt}</option>)}
          </select>
          <input
            placeholder="Search tickets..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            style={{ background: '#1f2933', color: '#e5e7eb', border: 'none', borderRadius: 6, padding: 8, fontSize: 15, minWidth: 180 }}
          />
          <select value={sortBy} onChange={e => setSortBy(e.target.value)} style={{ background: '#1f2933', color: '#e5e7eb', border: 'none', borderRadius: 6, padding: 8, fontSize: 15 }}>
            <option value="created_at">Sort by Date</option>
            <option value="status">Sort by Status</option>
          </select>
          <select value={sortDir} onChange={e => setSortDir(e.target.value)} style={{ background: '#1f2933', color: '#e5e7eb', border: 'none', borderRadius: 6, padding: 8, fontSize: 15 }}>
            <option value="desc">Desc</option>
            <option value="asc">Asc</option>
          </select>
        </div>

        {loading ? (
          <LoadingSpinner />
        ) : error ? (
          <div style={{ color: '#ef4444', marginBottom: 16 }}>{error}</div>
        ) : filtered.length === 0 ? (
          <div style={{ color: '#94a3b8' }}>No tickets found.</div>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', background: '#1f2933', borderRadius: 12, borderCollapse: 'collapse', marginBottom: 24 }}>
              <thead>
                <tr style={{ background: '#111827', color: '#e5e7eb' }}>
                  <th style={thStyle}>#</th>
                  <th style={thStyle}>Title</th>
                  <th style={thStyle}>Category</th>
                  <th style={thStyle}>Confidence</th>
                  <th style={thStyle}>Status</th>
                  <th style={thStyle}>Created</th>
                  <th style={thStyle}>User</th>
                  <th style={thStyle}></th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((t) => (
                  <tr key={t.ticket_number} style={{ borderBottom: '1px solid #334155' }}>
                    <td style={tdStyle}>{t.ticket_number}</td>
                    <td style={tdStyle}>{t.title}</td>
                    <td style={tdStyle}>{t.category}</td>
                    <td style={tdStyle}>{(t.confidence * 100).toFixed(1)}%</td>
                    <td style={tdStyle}><StatusBadge status={t.status} /></td>
                    <td style={tdStyle}>{new Date(t.created_at).toLocaleString()}</td>
                    <td style={tdStyle}>{t.user_id}</td>
                    <td style={tdStyle}>
                      <button onClick={() => setSelectedTicket(t)} style={{ background: '#3b82f6', color: '#e5e7eb', border: 'none', borderRadius: 6, padding: '4px 14px', fontWeight: 500, cursor: 'pointer' }}>View</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        <TicketDetailView ticket={selectedTicket} onClose={() => setSelectedTicket(null)} />
      </div>
    </div>
  );
}

const thStyle = { padding: 12, textAlign: 'left', fontWeight: 600, fontSize: 15 };
const tdStyle = { padding: 10, fontSize: 15 };
