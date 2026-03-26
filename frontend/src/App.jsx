import { useState, useEffect } from "react";
import Login from "./pages/Login";
import UserDashboard from "./pages/UserDashboard";
import AdminDashboard from "./pages/AdminDashboard";

function App() {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem("user");
    return saved ? JSON.parse(saved) : null;
  });

  useEffect(() => {
    if (user) {
      localStorage.setItem("user", JSON.stringify(user));
    } else {
      localStorage.removeItem("user");
    }
  }, [user]);

  if (!user) return (
    <div style={{ background: '#0f172a', minHeight: '100vh' }}>
      <Login setUser={setUser} />
    </div>
  );

  if (user.role === "ADMIN") {
    return (
      <div style={{ background: '#0f172a', minHeight: '100vh' }}>
        <AdminDashboard user={user} />
      </div>
    );
  }

  return (
    <div style={{ background: '#0f172a', minHeight: '100vh' }}>
      <UserDashboard user={user} />
    </div>
  );
}

export default App;
