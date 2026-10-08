import axios from 'axios';

const api = axios.create({
  baseURL: 'http://10.135.60.21:3000/', // Substitua pelo IP Local
});

export default api;