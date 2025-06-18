// src/api/axios.ts
import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL, // 👈 pulls from .env
  withCredentials: false, // adjust if you're handling cookies
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;