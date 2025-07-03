// pages/Login.tsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import {
  TextInput,
  PasswordInput,
  Button,
  Paper,
  Title,
  Stack,
  Text,
  Container,
} from '@mantine/core';

interface Props {
  setToken: (token: string) => void;
}

const Login = ({ setToken }: Props) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async () => {
    setError('');
    try {
      const response = await axios.post(`${import.meta.env.VITE_API_URL}/auth/login`, {
        email,
        password,
      });

      const token = response.data.access_token;
      localStorage.setItem('token', token);
      setToken(token);
      console.log('Login successful, navigating to dashboard...');
      navigate('/dashboard');
    } catch (err) {
      console.error('Login failed', err);
      setError('Invalid email or password');
    }
  };

  return (
    <Container size={420} my={80}>
      <Title style={{ textAlign: 'center' }} mb="md">
        Login
      </Title>

      <Paper withBorder shadow="md" p="xl" radius="md">
        <Stack>
          <TextInput
            label="Email"
            placeholder="you@example.com"
            required
            value={email}
            onChange={(e) => setEmail(e.currentTarget.value)}
          />

          <PasswordInput
            label="Password"
            placeholder="Your password"
            required
            value={password}
            onChange={(e) => setPassword(e.currentTarget.value)}
          />

          {error && <Text color="red" size="sm">{error}</Text>}

          <Button fullWidth mt="md" onClick={handleLogin}>
            Login
          </Button>
        </Stack>
      </Paper>
    </Container>
  );
};

export default Login;