// src/pages/Dashboard.tsx
import { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Button, Title, Text, Stack, Container } from '@mantine/core';

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

  if (!user) return <Text>Loading...</Text>;

  return (
    <Container size="sm" py="xl">
      <Stack>
        <Title order={2}>Welcome to your Dashboard</Title>
        <Text>User ID: {user.user_id}</Text>
        <Text>Role: {user.role}</Text>

        <Button color="blue" onClick={() => navigate('/upload')}>
          Upload New File
        </Button>
      </Stack>
    </Container>
  );
};

export default Dashboard;