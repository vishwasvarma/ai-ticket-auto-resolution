import { useState } from "react";
import Login from "./pages/Login";
import UserDashboard from "./pages/UserDashboard";
import AdminDashboard from "./pages/AdminDashboard";

function App() {
  const [user, setUser] = useState(null);

  if (!user) return <Login setUser={setUser} />;

  if (user.role === "ADMIN") {
    return <AdminDashboard user={user} />;
  }

  return <UserDashboard user={user} />;
}

export default App;
