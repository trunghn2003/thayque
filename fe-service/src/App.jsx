import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import AppointmentPage from './pages/AppointmentPage.jsx';
import PatientRecordPage from './pages/PatientRecordPage.jsx';
import MedicationHistoryPage from './pages/MedicationHistoryPage.jsx';
import ReminderPage from './pages/ReminderPage.jsx';
import LoginPage from './pages/LoginPage.jsx';
import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const userType = localStorage.getItem('user_type');
  const token = localStorage.getItem('token');

  return (
    <Router>
      {!token ? (
        <LoginPage />
      ) : (
        <div style={{padding: 24}}>
          <h2>Hệ thống quản lý bệnh viện</h2>
          <nav style={{marginBottom: 24}}>
            {/* Ẩn/hiện menu theo role */}
            <Link to="/appointments" style={{marginRight: 16}}>Lịch hẹn</Link>
            <Link to="/patient-records" style={{marginRight: 16}}>Hồ sơ bệnh án</Link>
            <Link to="/medication-history" style={{marginRight: 16}}>Lịch sử khám/đơn thuốc</Link>
            <Link to="/reminders">Nhắc nhở</Link>
          </nav>
          <Routes>
            <Route path="/appointments" element={<AppointmentPage />} />
            <Route path="/patient-records" element={<PatientRecordPage />} />
            <Route path="/medication-history" element={<MedicationHistoryPage />} />
            <Route path="/reminders" element={<ReminderPage />} />
            <Route path="*" element={<div>Chào mừng đến với hệ thống quản lý bệnh viện.<br/>Chọn chức năng ở menu trên.</div>} />
          </Routes>
        </div>
      )}
    </Router>
  )
}

export default App
