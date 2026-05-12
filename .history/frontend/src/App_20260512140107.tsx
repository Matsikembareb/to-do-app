import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<div>Home</div>} />
      </Routes>
    </Router>
  );
}

