// App.tsx
import { Routes, Route, Navigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import UploadPage from './pages/UploadForm';

function App() {
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const saved = localStorage.getItem('token');
    if (saved) setToken(saved);
  }, []);

  return (
    <Routes>
      <Route path="/" element={<Login setToken={setToken} />} />
      <Route path="/dashboard" element={token ? <Dashboard /> : <Navigate to="/" />} />
      <Route path="/upload" element={<UploadPage />} />
    </Routes>
  );
}

export default App;