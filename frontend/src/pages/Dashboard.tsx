// src/pages/Dashboard.tsx
import { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const [user, setUser] = useState<{ user_id: string; role: string } | null>(null);
  const navigate = useNavigate();

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
    <div className="p-6">
      <h2 className="text-3xl font-bold mb-4">Welcome to your Dashboard</h2>
      <p className="mb-2">User ID: {user.user_id}</p>
      <p className="mb-4">Role: {user.role}</p>

      {/* Upload Button */}
      <button
        onClick={() => navigate('/upload')}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Upload New File
      </button>
    </div>
  );
};

export default Dashboard;