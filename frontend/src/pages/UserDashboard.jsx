import { useEffect, useState } from "react";
import API from "../services/api";
import TicketCard from "../components/TicketCard";
import LoadingSpinner from "../components/LoadingSpinner";
import DashboardStatsCards from "../components/DashboardStatsCards";
import TicketDetailView from "../components/TicketDetailView";

export default function UserDashboard({ user }) {
  const [tickets, setTickets] = useState([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [creating, setCreating] = useState(false);
  const [selectedTicket, setSelectedTicket] = useState(null);

  const fetchTickets = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await API.get("/tickets/my", {
        headers: { user_id: user.user_id },
      });
      setTickets(res.data);
    } catch (err) {
      setError("Failed to fetch tickets");
    }
    setLoading(false);
  };

  const createTicket = async () => {
    if (!title || !description) return setError("Title and description required");
    setCreating(true);
    setError("");
    try {
      await API.post(
        "/tickets/create",
        { title, description },
        { headers: { user_id: user.user_id } },
      );
      setTitle("");
      setDescription("");
      fetchTickets();
    } catch (err) {
      setError("Failed to create ticket");
    }
    setCreating(false);
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

  return (
    <div style={{ background: '#0f172a', minHeight: '100vh', color: '#e5e7eb', padding: 0 }}>
      <div style={{ maxWidth: 700, margin: '0 auto', padding: 24 }}>
        <h2 style={{ fontWeight: 700, fontSize: 28, marginBottom: 10 }}>User Dashboard</h2>
        <DashboardStatsCards stats={stats} />

        <div style={{ background: '#1f2933', borderRadius: 12, padding: 20, marginBottom: 28 }}>
          <h3 style={{ fontWeight: 600, fontSize: 20, marginBottom: 10 }}>Create Ticket</h3>
          <input
            placeholder="Title"
            value={title}
            onChange={e => setTitle(e.target.value)}
            style={{ width: '100%', marginBottom: 10, padding: 10, borderRadius: 6, border: 'none', background: '#111827', color: '#e5e7eb' }}
            disabled={creating}
          />
          <textarea
            placeholder="Description"
            value={description}
            onChange={e => setDescription(e.target.value)}
            style={{ width: '100%', marginBottom: 10, padding: 10, borderRadius: 6, border: 'none', background: '#111827', color: '#e5e7eb', minHeight: 60 }}
            disabled={creating}
          />
          <button
            onClick={createTicket}
            style={{ background: '#3b82f6', color: '#e5e7eb', border: 'none', borderRadius: 6, padding: '8px 24px', fontWeight: 600, cursor: 'pointer', fontSize: 16 }}
            disabled={creating}
          >
            {creating ? 'Creating...' : 'Create Ticket'}
          </button>
          {error && <div style={{ color: '#ef4444', marginTop: 10 }}>{error}</div>}
        </div>

        <h3 style={{ fontWeight: 600, fontSize: 20, marginBottom: 10 }}>My Tickets</h3>
        {loading ? (
          <LoadingSpinner />
        ) : error ? (
          <div style={{ color: '#ef4444', marginBottom: 16 }}>{error}</div>
        ) : tickets.length === 0 ? (
          <div style={{ color: '#94a3b8' }}>No tickets found.</div>
        ) : (
          <div>
            {tickets.map((t) => (
              <TicketCard key={t.ticket_number} ticket={t} onExpand={setSelectedTicket} />
            ))}
          </div>
        )}
        <TicketDetailView ticket={selectedTicket} onClose={() => setSelectedTicket(null)} />
      </div>
    </div>
  );
}
