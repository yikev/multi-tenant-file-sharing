import {
  Title,
  Text,
  Container,
  SimpleGrid,
  Card,
  Group,
  Stack,
} from '@mantine/core';
import { useEffect, useState } from 'react';
import { StatsRingCard } from '../components/StatsRingCard';
import axios from 'axios';

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState<any>(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    axios
      .get(`${import.meta.env.VITE_API_URL}/dashboard`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => setDashboardData(res.data))
      .catch((err) => console.error('Failed to fetch dashboard data', err));
  }, []);

  if (!dashboardData) return <Text>Loading...</Text>;

  return (
    <Container size="lg" py="xl">
      <Title order={2} mb="lg">Dashboard</Title>

      <SimpleGrid cols={{ base: 1, sm: 2 }} spacing="lg">
        {/* Recent Uploads */}
        <Card shadow="sm" padding="md" withBorder>
          <Title order={3}>Recent Uploads</Title>
          <Stack mt="sm" gap="xs">
            {dashboardData.recent_files.map((file: any) => (
              <Text key={file.id}>{file.filename} - {file.filesize_kb} KB</Text>
            ))}
          </Stack>
        </Card>

        {/* Recent Projects */}
        <Card shadow="sm" padding="md" withBorder>
          <Title order={3}>Recent Projects</Title>
          <Stack mt="sm" gap="xs">
            {dashboardData.recent_projects.map((project: any) => (
              <Text key={project.id}>{project.name}</Text>
            ))}
          </Stack>
        </Card>

        {/* Stats */}
        <Card shadow="sm" padding="md" withBorder>
          <Title order={3}>Stats</Title>
          <StatsRingCard
            totalFiles={dashboardData.total_files}
            totalStorageKB={dashboardData.total_storage_kb}
            totalUsers={dashboardData.total_users}
          />
        </Card>

        {/* Activity Log - Placeholder */}
        <Card shadow="sm" padding="md" withBorder>
          <Title order={3}>Activity Log</Title>
          <Text>Coming soon...</Text>
        </Card>
      </SimpleGrid>
    </Container>
  );
};

export default Dashboard;