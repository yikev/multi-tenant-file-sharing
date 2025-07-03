import React from 'react';
import ReactDOM from 'react-dom/client';
import { HashRouter } from 'react-router-dom';
import { MantineProvider } from '@mantine/core';
import App from './App.tsx';
import './index.css';
import { ProjectProvider } from './context/ProjectContext';
import '@mantine/core/styles.css'

console.log("VITE_API_URL =", import.meta.env.VITE_API_URL);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <MantineProvider>
      <ProjectProvider>
        <HashRouter>
          <App />
        </HashRouter>
      </ProjectProvider>
    </MantineProvider>
  </React.StrictMode>
);