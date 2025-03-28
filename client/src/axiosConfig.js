import axios from 'axios';

const baseURL = process.env.NODE_ENV === 'production'
  ? 'https://ethandixon03.pythonanywhere.com'
  : 'http://localhost:5000';

const instance = axios.create({
  baseURL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default instance; 