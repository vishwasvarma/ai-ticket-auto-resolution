import { useEffect, useState } from "react";
import API from "../services/api";

export default function UserDashboard({ user }) {
  const [tickets, setTickets] = useState([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [aiResponse, setAiResponse] = useState(null);

  const fetchTickets = async () => {
    const res = await API.get("/tickets/my");
    setTickets(res.data);
  };

  const createTicket = async () => {
    if (!title || !description) {
      alert("Enter title and description");
      return;
    }

    const res = await API.post("/tickets/create", { title, description });

    setAiResponse(res.data);
    setTitle("");
    setDescription("");
    fetchTickets();
  };

  useEffect(() => {
    fetchTickets();
  }, []);

  return (
    <div
      style={{
        padding: "30px",
        background: "#0f172a",
        minHeight: "100vh",
        color: "white",
      }}
    >
      {/* HEADER */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginBottom: "20px",
        }}
      >
        <h1>User Dashboard</h1>
        <button
          onClick={() => {
            localStorage.removeItem("token");
            window.location.reload();
          }}
        >
          Logout
        </button>
      </div>

      {/* CREATE TICKET CARD */}
      <div
        style={{
          background: "#1e293b",
          padding: "20px",
          borderRadius: "10px",
          marginBottom: "20px",
        }}
      >
        <h2>Create New Ticket</h2>

        <input
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          style={{ width: "100%", padding: "10px", margin: "10px 0" }}
        />

        <textarea
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          style={{ width: "100%", padding: "10px", margin: "10px 0" }}
        />

        <button onClick={createTicket}>Submit Ticket</button>
      </div>

      {/* AI RESPONSE */}
      {aiResponse && (
        <div
          style={{
            background: "#1e293b",
            padding: "20px",
            borderRadius: "10px",
            marginBottom: "20px",
          }}
        >
          <h2>AI Resolution</h2>
          <p>
            <b>Category:</b> {aiResponse.category}
          </p>
          <p>
            <b>Response:</b> {aiResponse.response}
          </p>
          <p>
            <b>Ticket ID:</b> {aiResponse.ticket_number}
          </p>
        </div>
      )}

      {/* MY TICKETS */}
      <div>
        <h2>My Tickets</h2>

        {tickets.map((t) => (
          <div
            key={t.ticket_number}
            style={{
              background: "#1e293b",
              padding: "15px",
              borderRadius: "10px",
              marginTop: "10px",
            }}
          >
            <h3>{t.title}</h3>
            <p>Status: {t.status}</p>
            <p>Category: {t.category}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
