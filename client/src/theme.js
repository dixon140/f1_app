import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#ff1744', // A bright red color
      light: '#ff4569',
      dark: '#b2102f',
    },
    secondary: {
      main: '#ff4081', // A lighter red/pink color
      light: '#ff79b0',
      dark: '#c60055',
    },
    background: {
      default: '#000000',
      paper: '#1a1a1a',
    },
    text: {
      primary: '#ffffff',
      secondary: '#b3b3b3',
    },
    error: {
      main: '#ff1744',
    },
  },
  components: {
    MuiTableHead: {
      styleOverrides: {
        root: {
          backgroundColor: '#1a1a1a',
          '& .MuiTableCell-head': {
            color: '#ff1744',
            fontWeight: 'bold',
          },
        },
      },
    },
    MuiTableRow: {
      styleOverrides: {
        root: {
          '&:nth-of-type(odd)': {
            backgroundColor: '#0a0a0a',
          },
          '&:hover': {
            backgroundColor: '#2a2a2a !important',
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 4,
        },
        containedPrimary: {
          color: '#ffffff',
        },
      },
    },
    MuiIconButton: {
      styleOverrides: {
        root: {
          color: '#ff1744',
          '&:hover': {
            backgroundColor: 'rgba(255, 23, 68, 0.1)',
          },
        },
      },
    },
  },
});

export default theme; 