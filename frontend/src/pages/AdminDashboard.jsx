import { useEffect, useState } from "react";
import API from "../services/api";

export default function AdminDashboard({ user }) {
  const [tickets, setTickets] = useState([]);

  const fetchTickets = async () => {
    const res = await API.get("/tickets", {
      headers: { user_id: user.user_id },
    });
    setTickets(res.data);
  };

  useEffect(() => {
    fetchTickets();
  }, []);

  return (
    <div>
      <h2>Admin Dashboard</h2>

      {tickets.map((t) => (
        <div key={t.ticket_number}>
          <p>
            {t.title} - {t.status}
          </p>
        </div>
      ))}
    </div>
  );
}
