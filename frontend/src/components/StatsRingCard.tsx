import { Card, Group, RingProgress, Text, useMantineTheme } from '@mantine/core';
import classes from './StatsRingCard.module.css';

const stats = [
  { value: 447, label: 'Remaining' },
  { value: 76, label: 'In progress' },
];

type StatsRingCardProps = {
  totalFiles: number;
  totalStorageKB: number;
  totalUsers: number;
};

export function StatsRingCard({ totalFiles, totalStorageKB, totalUsers }: StatsRingCardProps) {
  const theme = useMantineTheme();

  const completed = totalFiles;
  const total = totalFiles + 100; // or whatever total you'd like for ring % base

  const stats = [
    { value: totalStorageKB, label: 'Storage (KB)' },
    { value: totalUsers, label: 'Users' },
  ];

  const items = stats.map((stat) => (
    <div key={stat.label}>
      <Text className={classes.label}>{stat.value}</Text>
      <Text size="xs" c="dimmed">
        {stat.label}
      </Text>
    </div>
  ));

  return (
    <Card withBorder p="xl" radius="md" className={classes.card}>
      <div className={classes.inner}>
        <div>
          <Text fz="xl" className={classes.label}>
            Stats
          </Text>
          <div>
            <Text className={classes.lead} mt={30}>
              {totalFiles}
            </Text>
            <Text fz="xs" c="dimmed">
              Total Files
            </Text>
          </div>
          <Group mt="lg">{items}</Group>
        </div>

        <div className={classes.ring}>
          <RingProgress
            roundCaps
            thickness={6}
            size={150}
            sections={[{ value: (completed / total) * 100, color: theme.primaryColor }]}
            label={
              <div>
                <Text ta="center" fz="lg" className={classes.label}>
                  {((completed / total) * 100).toFixed(0)}%
                </Text>
                <Text ta="center" fz="xs" c="dimmed">
                  Completed
                </Text>
              </div>
            }
          />
        </div>
      </div>
    </Card>
  );
}