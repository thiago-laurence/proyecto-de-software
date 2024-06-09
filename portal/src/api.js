import axios from 'axios'

let url_api = ''

if (import.meta.url.includes('localhost')) {
  // url_api = 'https://localhost:5000/api/'
  url_api = 'http://localhost:5000/api/'
}else{
  url_api = 'https://admin-grupo10.proyecto2023.linti.unlp.edu.ar/api/'
}

const API = axios.create({
    baseURL: url_api
});

API.interceptors.request.use(config => {
  const token = localStorage.getItem('jwt');
  config.headers.Authorization = `Bearer ${token}`;
  config.headers['Content-Type'] = 'application/json';

  return config;
}, error => {
  return Promise.reject(error);
});


export { API };