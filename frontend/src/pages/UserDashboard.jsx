import { useEffect, useState } from "react";
import API from "../services/api";

export default function UserDashboard({ user }) {
  const [tickets, setTickets] = useState([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  const fetchTickets = async () => {
    const res = await API.get("/tickets/my", {
      headers: { user_id: user.user_id },
    });
    setTickets(res.data);
  };

  const createTicket = async () => {
    await API.post(
      "/tickets/create",
      { title, description },
      { headers: { user_id: user.user_id } },
    );
    fetchTickets();
  };

  useEffect(() => {
    fetchTickets();
  }, []);

  return (
    <div>
      <h2>User Dashboard</h2>

      <input placeholder="Title" onChange={(e) => setTitle(e.target.value)} />
      <input
        placeholder="Description"
        onChange={(e) => setDescription(e.target.value)}
      />
      <button onClick={createTicket}>Create Ticket</button>

      <h3>My Tickets</h3>
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
