import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import logo from './logo.svg';
import './App.css';

// Placeholder components (to be implemented)
const MainPage = React.lazy(() => import('./MainPage'));
const FormPage = React.lazy(() => import('./FormPage'));
const ProcessedInfoPage = React.lazy(() => import('./ProcessedInfoPage'));

function App() {
  return (
    <Router>
      <React.Suspense fallback={<div>Loading...</div>}>
        <Routes>
          <Route path="/" element={<MainPage />} />
          <Route path="/form" element={<FormPage />} />
          <Route path="/results" element={<ProcessedInfoPage />} />
        </Routes>
      </React.Suspense>
    </Router>
  );
}

export default App;
