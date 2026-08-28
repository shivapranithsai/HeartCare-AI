import { Routes, Route, Navigate } from "react-router-dom";

import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import NewPrediction from "./pages/NewPrediction";
import PredictionResult from "./pages/PredictionResult";
import History from "./pages/History";
import Hospitals from "./pages/Hospitals";
import Reports from "./pages/Reports";
import Profile from "./pages/Profile";

function App() {
  return (
    <Routes>
      {/* PUBLIC HOME & AUTH */}
      <Route path="/" element={<Landing />} />
      <Route path="/login" element={<Login />} />

      {/* CORE CLINICAL SUITE */}
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/new-prediction" element={<NewPrediction />} />
      <Route path="/prediction-result" element={<PredictionResult />} />
      <Route path="/history" element={<History />} />
      <Route path="/hospitals" element={<Hospitals />} />
      <Route path="/reports" element={<Reports />} />
      <Route path="/profile" element={<Profile />} />

      {/* FALLBACK REDIRECT */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;