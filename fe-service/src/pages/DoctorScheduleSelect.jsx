import React, { useEffect, useState } from "react";

// Component chọn bác sĩ, ngày, slot
export default function DoctorScheduleSelect({ onSelect }) {
  const [schedules, setSchedules] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selected, setSelected] = useState("");

  useEffect(() => {
    const fetchSchedules = async () => {
      setLoading(true);
      setError("");
      try {
        const res = await fetch("http://localhost:8001/api/doctor-schedules/");
        const data = await res.json();
        if (res.status === 200) setSchedules(data);
        else setError("Không lấy được lịch làm việc bác sĩ");
      } catch {
        setError("Lỗi kết nối appointment_service");
      }
      setLoading(false);
    };
    fetchSchedules();
  }, []);

  const handleChange = e => {
    setSelected(e.target.value);
    if (onSelect) onSelect(e.target.value);
  };

  if (loading) return <div>Đang tải lịch làm việc bác sĩ...</div>;
  if (error) return <div style={{color:'red'}}>{error}</div>;
  return (
    <select value={selected} onChange={handleChange} required>
      <option value="">-- Chọn bác sĩ & thời gian --</option>
      {schedules.map(s => (
        <option key={s.id} value={s.id}>
          Bác sĩ ID {s.doctor_id} | {new Date(s.start_time).toLocaleString()} - {new Date(s.end_time).toLocaleTimeString()}
        </option>
      ))}
    </select>
  );
}
