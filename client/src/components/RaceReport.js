import React, { useState, useEffect } from 'react';
import {
    Container,
    Paper,
    Typography,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Box,
    CircularProgress,
    Button,
    Grid
} from '@mui/material';
import { useParams } from 'react-router-dom';
import axios from '../axiosConfig';
import PrintIcon from '@mui/icons-material/Print';

function RaceReport() {
    const [raceReport, setRaceReport] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const { raceId } = useParams();

    useEffect(() => {
        const fetchRaceReport = async () => {
            try {
                setLoading(true);
                const response = await axios.get(`/api/races/${raceId}/report`);
                setRaceReport(response.data);
                setLoading(false);
            } catch (err) {
                setError('Failed to fetch race report: ' + (err.response?.data?.error || err.message));
                setLoading(false);
            }
        };

        if (raceId) {
            fetchRaceReport();
        }
    }, [raceId]);

    const handlePrint = () => {
        window.print();
    };

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

    if (!raceReport) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
                <Typography>No race data available</Typography>
            </Box>
        );
    }

    return (
        <Container maxWidth="lg" sx={{ py: 4 }}>
            <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
                <Typography variant="h4" component="h1">
                    {raceReport.race_details.name} {raceReport.race_details.season}
                </Typography>
                <Button
                    variant="contained"
                    startIcon={<PrintIcon />}
                    onClick={handlePrint}
                    sx={{ '@media print': { display: 'none' } }}
                >
                    Print Report
                </Button>
            </Box>

            <Grid container spacing={3} mb={4}>
                <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2 }}>
                        <Typography variant="h6" gutterBottom>Race Details</Typography>
                        <Table size="small">
                            <TableBody>
                                <TableRow>
                                    <TableCell component="th">Date</TableCell>
                                    <TableCell>{raceReport.race_details.date}</TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell component="th">Weather</TableCell>
                                    <TableCell>{raceReport.race_details.weather_conditions}</TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell component="th">Safety Car Appearances</TableCell>
                                    <TableCell>{raceReport.race_details.safety_car_appearances}</TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell component="th">Red Flags</TableCell>
                                    <TableCell>{raceReport.race_details.red_flags}</TableCell>
                                </TableRow>
                            </TableBody>
                        </Table>
                    </Paper>
                </Grid>
            </Grid>

            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Pos</TableCell>
                            <TableCell>Driver</TableCell>
                            <TableCell>Number</TableCell>
                            <TableCell>Team</TableCell>
                            <TableCell>Grid</TableCell>
                            <TableCell>Points</TableCell>
                            <TableCell>Status</TableCell>
                            <TableCell>Gap to Leader</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {raceReport.results.map((result) => (
                            <TableRow key={result.driver.code}>
                                <TableCell>{result.performance.finish_position}</TableCell>
                                <TableCell>
                                    <Box>
                                        <Typography variant="body1">
                                            {result.driver.name} ({result.driver.code})
                                        </Typography>
                                        <Typography variant="caption" color="text.secondary">
                                            {result.driver.nationality}
                                        </Typography>
                                    </Box>
                                </TableCell>
                                <TableCell>{result.driver.number}</TableCell>
                                <TableCell>
                                    <Box>
                                        <Typography variant="body1">
                                            {result.team.name}
                                        </Typography>
                                        <Typography variant="caption" color="text.secondary">
                                            {result.team.nationality}
                                        </Typography>
                                    </Box>
                                </TableCell>
                                <TableCell>{result.performance.grid_position}</TableCell>
                                <TableCell>{result.performance.points_earned}</TableCell>
                                <TableCell>{result.performance.status}</TableCell>
                                <TableCell>{result.performance.gap_to_leader}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </Container>
    );
}

export default RaceReport; 