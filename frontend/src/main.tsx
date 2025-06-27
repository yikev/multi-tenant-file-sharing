import React from 'react';
import ReactDOM from 'react-dom/client';
import { HashRouter } from 'react-router-dom';
import App from './App.tsx';
import './index.css';
import { ProjectProvider } from './context/ProjectContext'; // 👈 import this

console.log("VITE_API_URL =", import.meta.env.VITE_API_URL);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ProjectProvider> {/* 👈 wrap App inside */}
      <HashRouter>
        <App />
      </HashRouter>
    </ProjectProvider>
  </React.StrictMode>
);