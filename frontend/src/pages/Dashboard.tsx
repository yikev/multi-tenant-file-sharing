// src/pages/Dashboard.tsx
import { useEffect, useState } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [user, setUser] = useState<{ user_id: string; role: string } | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    axios
      .get(`${import.meta.env.VITE_API_URL}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => setUser(res.data))
      .catch((err) => {
        console.error('Unauthorized or token expired', err);
        setUser(null);
      });
  }, []);

  if (!user) return <p>Loading...</p>;

  return (
    <div>
      <h2>Welcome to your Dashboard</h2>
      <p>User ID: {user.user_id}</p>
      <p>Role: {user.role}</p>
    </div>
  );
};

export default Dashboard;