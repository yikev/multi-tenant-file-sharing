import {
  AppShell,
  AppShellHeader,
  AppShellNavbar,
  AppShellMain,
  Burger,
  Text,
} from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { Routes, Route, useLocation } from 'react-router-dom';
import { NavbarSimpleColored } from './components/NavbarSimpleColored';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import UploadPage from './pages/UploadForm';
import { useState } from 'react';

export default function App() {
  const [token, setToken] = useState<string | null>(null);
  const [opened, { toggle }] = useDisclosure();
  const location = useLocation();

  // Only show navbar on non-login routes
  const showNavbar = location.pathname !== '/';

  return (
    <AppShell
      header={{ height: 60 }}
      navbar={
        showNavbar
          ? {
              width: 300,
              breakpoint: 'sm',
              collapsed: { mobile: !opened },
            }
          : undefined
      }
      padding="md"
    >
      <AppShellHeader>
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            height: '100%',
            padding: '0 16px',
          }}
        >
          {showNavbar && (
            <Burger opened={opened} onClick={toggle} hiddenFrom="sm" size="sm" />
          )}
          <Text fw={700} ml={showNavbar ? 'md' : 0}>
            Multi-Tenant File Sharing
          </Text>
        </div>
      </AppShellHeader>

      {showNavbar && (
        <AppShellNavbar p={0}>
          <NavbarSimpleColored />
        </AppShellNavbar>
      )}

      <AppShellMain>
        <Routes>
          <Route path="/" element={<Login setToken={setToken} />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/upload" element={<UploadPage />} />
        </Routes>
      </AppShellMain>
    </AppShell>
  );
}