import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';

const RaceResults = ({ isAdmin }) => {
  const [results, setResults] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingResult, setEditingResult] = useState(null);
  const [races, setRaces] = useState([]);
  const [drivers, setDrivers] = useState([]);
  const [teams, setTeams] = useState([]);
  const [formData, setFormData] = useState({
    race_id: '',
    driver_id: '',
    team_id: '',
    car_id: '',
    grid_position: '',
    finish_position: '',
    points_earned: '',
    laps_completed: '',
    status: 'Finished',
    gap_to_leader: '',
  });

  // Fetch race results
  const fetchResults = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/race-results');
      if (response.ok) {
        const data = await response.json();
        setResults(data);
      }
    } catch (error) {
      console.error('Error fetching race results:', error);
    }
  };

  // Fetch dropdown data
  const fetchDropdownData = async () => {
    try {
      const [racesRes, driversRes, teamsRes] = await Promise.all([
        fetch('http://localhost:5000/api/races'),
        fetch('http://localhost:5000/api/drivers'),
        fetch('http://localhost:5000/api/teams')
      ]);

      if (racesRes.ok && driversRes.ok && teamsRes.ok) {
        const [racesData, driversData, teamsData] = await Promise.all([
          racesRes.json(),
          driversRes.json(),
          teamsRes.json()
        ]);

        setRaces(racesData);
        setDrivers(driversData);
        setTeams(teamsData);
      }
    } catch (error) {
      console.error('Error fetching dropdown data:', error);
    }
  };

  // Fetch driver's current team and car
  const fetchDriverTeamAndCar = async (driverId) => {
    try {
      const response = await fetch(`http://localhost:5000/api/drivers/${driverId}/current-team`);
      if (response.ok) {
        const data = await response.json();
        setFormData(prev => ({
          ...prev,
          team_id: data.team_id,
          car_id: data.car_id
        }));
      }
    } catch (error) {
      console.error('Error fetching driver team and car:', error);
    }
  };

  useEffect(() => {
    fetchResults();
    fetchDropdownData();
  }, []);

  const handleOpenDialog = (result = null) => {
    if (result) {
      setEditingResult(result);
      setFormData(result);
    } else {
      setEditingResult(null);
      setFormData({
        race_id: '',
        driver_id: '',
        team_id: '',
        car_id: '',
        grid_position: '',
        finish_position: '',
        points_earned: '',
        laps_completed: '',
        status: 'Finished',
        gap_to_leader: '',
      });
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingResult(null);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // If driver is selected, fetch their current team and car
    if (name === 'driver_id' && value) {
      fetchDriverTeamAndCar(value);
    }
  };

  const handleSubmit = async () => {
    try {
      const url = editingResult
        ? `http://localhost:5000/api/race-results/${editingResult.result_id}`
        : 'http://localhost:5000/api/race-results';
      
      const response = await fetch(url, {
        method: editingResult ? 'PUT' : 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        fetchResults();
        handleCloseDialog();
      } else {
        const error = await response.json();
        alert(error.error || 'An error occurred');
      }
    } catch (error) {
      console.error('Error saving race result:', error);
      alert('An error occurred while saving the race result');
    }
  };

  const handleDelete = async (resultId) => {
    if (!window.confirm('Are you sure you want to delete this race result?')) {
      return;
    }

    try {
      const response = await fetch(`http://localhost:5000/api/race-results/${resultId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        fetchResults();
      } else {
        const error = await response.json();
        alert(error.error || 'An error occurred while deleting');
      }
    } catch (error) {
      console.error('Error deleting race result:', error);
      alert('An error occurred while deleting the race result');
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
        <h2>Race Results</h2>
        {isAdmin && (
          <Button variant="contained" color="primary" onClick={() => handleOpenDialog()}>
            Add New Result
          </Button>
        )}
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Race</TableCell>
              <TableCell>Driver</TableCell>
              <TableCell>Team</TableCell>
              <TableCell>Grid</TableCell>
              <TableCell>Finish</TableCell>
              <TableCell>Points</TableCell>
              <TableCell>Status</TableCell>
              {isAdmin && <TableCell>Actions</TableCell>}
            </TableRow>
          </TableHead>
          <TableBody>
            {results.map((result) => (
              <TableRow key={result.result_id}>
                <TableCell>{result.race_name}</TableCell>
                <TableCell>{result.driver_name}</TableCell>
                <TableCell>{result.team_name}</TableCell>
                <TableCell>{result.grid_position}</TableCell>
                <TableCell>
                  {result.status === 'Finished' ? result.finish_position : result.status}
                </TableCell>
                <TableCell>{result.points_earned}</TableCell>
                <TableCell>{result.status}</TableCell>
                {isAdmin && (
                  <TableCell>
                    <IconButton onClick={() => handleOpenDialog(result)}>
                      <EditIcon />
                    </IconButton>
                    <IconButton onClick={() => handleDelete(result.result_id)}>
                      <DeleteIcon />
                    </IconButton>
                  </TableCell>
                )}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>{editingResult ? 'Edit Race Result' : 'Add New Race Result'}</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, pt: 2 }}>
            <FormControl fullWidth>
              <InputLabel>Race</InputLabel>
              <Select
                name="race_id"
                value={formData.race_id}
                onChange={handleInputChange}
                label="Race"
              >
                {races.map((race) => (
                  <MenuItem key={race.race_id} value={race.race_id}>
                    {race.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <FormControl fullWidth>
              <InputLabel>Driver</InputLabel>
              <Select
                name="driver_id"
                value={formData.driver_id}
                onChange={handleInputChange}
                label="Driver"
              >
                {drivers.map((driver) => (
                  <MenuItem key={driver.driver_id} value={driver.driver_id}>
                    {driver.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <FormControl fullWidth>
              <InputLabel>Team</InputLabel>
              <Select
                name="team_id"
                value={formData.team_id}
                onChange={handleInputChange}
                label="Team"
                disabled
              >
                {teams.map((team) => (
                  <MenuItem key={team.team_id} value={team.team_id}>
                    {team.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <TextField
              name="grid_position"
              label="Grid Position"
              type="number"
              value={formData.grid_position}
              onChange={handleInputChange}
              fullWidth
            />
            <TextField
              name="finish_position"
              label="Finish Position"
              type="number"
              value={formData.finish_position}
              onChange={handleInputChange}
              fullWidth
            />
            <TextField
              name="points_earned"
              label="Points Earned"
              type="number"
              value={formData.points_earned}
              onChange={handleInputChange}
              fullWidth
            />
            <TextField
              name="laps_completed"
              label="Laps Completed"
              type="number"
              value={formData.laps_completed}
              onChange={handleInputChange}
              fullWidth
            />
            <FormControl fullWidth>
              <InputLabel>Status</InputLabel>
              <Select
                name="status"
                value={formData.status}
                onChange={handleInputChange}
                label="Status"
              >
                <MenuItem value="Finished">Finished</MenuItem>
                <MenuItem value="DNF">DNF</MenuItem>
                <MenuItem value="DSQ">DSQ</MenuItem>
                <MenuItem value="DNS">DNS</MenuItem>
              </Select>
            </FormControl>
            <TextField
              name="gap_to_leader"
              label="Gap to Leader"
              value={formData.gap_to_leader}
              onChange={handleInputChange}
              fullWidth
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSubmit} variant="contained" color="primary">
            {editingResult ? 'Save Changes' : 'Add Result'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default RaceResults; 