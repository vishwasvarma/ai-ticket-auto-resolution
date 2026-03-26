import { useState } from "react";
import API from "../services/api";

export default function Login({ setUser }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    if (!username || !password) {
      alert("Enter username and password");
      return;
    }

    try {
      const res = await API.post("/login", {
        username: username,
        password: password,
      });

      setUser(res.data);
    } catch (err) {
      console.log(err.response?.data);
      alert("Login failed");
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h2>AI Ticket Resolution</h2>
        <p style={{ color: "#9ca3af" }}>Login to continue</p>

        <input
          style={styles.input}
          placeholder="Enter username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          style={styles.input}
          type="password"
          placeholder="Enter password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button style={styles.button} onClick={handleLogin}>
          Login
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "#0f172a",
  },
  card: {
    background: "#1f2933",
    padding: "30px",
    borderRadius: "10px",
    width: "300px",
    textAlign: "center",
    color: "#e5e7eb",
  },
  input: {
    width: "100%",
    padding: "10px",
    margin: "10px 0",
    borderRadius: "6px",
    border: "1px solid #374151",
    background: "#111827",
    color: "#fff",
  },
  button: {
    width: "100%",
    padding: "10px",
    background: "#3b82f6",
    border: "none",
    borderRadius: "6px",
    color: "#fff",
    cursor: "pointer",
  },
};
