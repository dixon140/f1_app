import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Grid, 
  Paper, 
  Typography, 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow,
  CircularProgress,
  Box,
  Divider,
  List,
  ListItem,
  ListItemText,
  Tab,
  Tabs,
  AppBar,
  Button
} from '@mui/material';
import LogoutIcon from '@mui/icons-material/Logout';
import axios from '../axiosConfig';
import RaceResults from './RaceResults';
import { useAuth } from '../AuthContext';

const TabPanel = (props) => {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
      style={{ backgroundColor: '#000000' }}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
};

function a11yProps(index) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}

function Dashboard() {
  const { isAdmin, logout } = useAuth();
  const [value, setValue] = useState(0);
  const [driverStandings, setDriverStandings] = useState([]);
  const [constructorStandings, setConstructorStandings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [seasonStats, setSeasonStats] = useState({
    totalRaces: 0,
    totalSprints: 0,
    podiumFinishes: {},
    polePositions: {},
    sprintWins: {}
  });

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const handleLogout = async () => {
    await logout();
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch driver standings
        const driversResponse = await axios.get('/api/drivers/standings');
        setDriverStandings(driversResponse.data);

        // Fetch constructor standings
        const constructorsResponse = await axios.get('/api/teams/standings');
        setConstructorStandings(constructorsResponse.data);

        // Fetch season statistics
        const statsResponse = await axios.get('/api/season/statistics');
        setSeasonStats(statsResponse.data);

        setLoading(false);
      } catch (err) {
        console.error('Error details:', err.response || err);
        setError('Failed to fetch statistics: ' + (err.response?.data?.error || err.message));
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const StatCard = ({ title, value, subtitle }) => (
    <Paper elevation={2} sx={{ p: 2, textAlign: 'center', height: '100%' }}>
      <Typography variant="h4" component="div" sx={{ mb: 1 }}>
        {value}
      </Typography>
      <Typography variant="subtitle1" color="text.secondary">
        {title}
      </Typography>
      {subtitle && (
        <Typography variant="caption" color="text.secondary" display="block">
          {subtitle}
        </Typography>
      )}
    </Paper>
  );

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ width: '100%', bgcolor: 'background.default', minHeight: '100vh' }}>
      <AppBar position="static" sx={{ bgcolor: 'background.paper' }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', px: 2 }}>
          <Tabs 
            value={value} 
            onChange={handleChange} 
            textColor="primary"
            indicatorColor="primary"
            sx={{
              '& .MuiTab-root': {
                color: 'text.secondary',
                '&.Mui-selected': {
                  color: 'primary.main',
                },
              },
            }}
          >
            <Tab label="Driver Standings" />
            <Tab label="Constructor Standings" />
            <Tab label="Race Results" />
            <Tab label="Season Statistics" />
          </Tabs>
          <Button
            color="primary"
            onClick={handleLogout}
            startIcon={<LogoutIcon />}
          >
            Logout
          </Button>
        </Box>
      </AppBar>

      <TabPanel value={value} index={0}>
        <Typography variant="h6" component="h2" gutterBottom>
          Driver Standings
        </Typography>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Position</TableCell>
                <TableCell>Driver</TableCell>
                <TableCell>Points</TableCell>
                <TableCell>Wins</TableCell>
                <TableCell>Podiums</TableCell>
                <TableCell>Pole Positions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {driverStandings.map((driver, index) => (
                <TableRow key={driver.driver_id}>
                  <TableCell>{index + 1}</TableCell>
                  <TableCell>{driver.name}</TableCell>
                  <TableCell>{driver.total_points}</TableCell>
                  <TableCell>{driver.total_wins}</TableCell>
                  <TableCell>{driver.podiums}</TableCell>
                  <TableCell>{driver.pole_positions}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>

      <TabPanel value={value} index={1}>
        <Typography variant="h6" component="h2" gutterBottom>
          Constructor Standings
        </Typography>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Position</TableCell>
                <TableCell>Team</TableCell>
                <TableCell>Points</TableCell>
                <TableCell>Wins</TableCell>
                <TableCell>Podiums</TableCell>
                <TableCell>Pole Positions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {constructorStandings.map((team, index) => (
                <TableRow key={team.team_id}>
                  <TableCell>{index + 1}</TableCell>
                  <TableCell>{team.name}</TableCell>
                  <TableCell>{team.total_points}</TableCell>
                  <TableCell>{team.total_wins}</TableCell>
                  <TableCell>{team.podiums}</TableCell>
                  <TableCell>{team.pole_positions}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>

      <TabPanel value={value} index={2}>
        <RaceResults isAdmin={isAdmin} />
      </TabPanel>

      <TabPanel value={value} index={3}>
        <Typography variant="h6" component="h2" gutterBottom>
          Season Statistics
        </Typography>
        <Box sx={{ mb: 4 }}>
          <Typography variant="subtitle1">Total Races: {seasonStats.totalRaces}</Typography>
        </Box>
        
        <Typography variant="h6" gutterBottom>Pole Positions</Typography>
        <TableContainer component={Paper} sx={{ mb: 4 }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Driver</TableCell>
                <TableCell>Count</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {Object.entries(seasonStats.polePositions).map(([driver, count]) => (
                <TableRow key={driver}>
                  <TableCell>{driver}</TableCell>
                  <TableCell>{count}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        <Typography variant="h6" gutterBottom>Podium Finishes</Typography>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Driver</TableCell>
                <TableCell>Count</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {Object.entries(seasonStats.podiumFinishes).map(([driver, count]) => (
                <TableRow key={driver}>
                  <TableCell>{driver}</TableCell>
                  <TableCell>{count}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>
    </Box>
  );
}

export default Dashboard; 