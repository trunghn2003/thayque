import React, { useEffect, useState } from "react";

function AppointmentPage() {
  const [appointments, setAppointments] = useState([]);
  const [error, setError] = useState("");

  const fetchAppointments = async () => {
    setError("");
    try {
      const res = await fetch("http://localhost:8001/api/appointments/", {
        headers: { "Authorization": "Bearer " + localStorage.getItem("token") }
      });
      const data = await res.json();
      if (res.status === 200) setAppointments(data);
      else setError("Không lấy được danh sách lịch hẹn");
    } catch {
      setError("Lỗi kết nối appointment_service");
    }
  };

  useEffect(() => {
    fetchAppointments();
  }, []);

  return (
    <div>
      <h2>Danh sách lịch hẹn</h2>
      {error && <div style={{color: 'red'}}>{error}</div>}
      <ul>
        {appointments.length === 0 && <li>Không có lịch hẹn nào.</li>}
        {appointments.map(a => (
          <li key={a.id} style={{marginBottom: 8}}>
            <b>Bác sĩ:</b> {a.doctor_id} | <b>Bệnh nhân:</b> {a.patient_id} | <b>Thời gian:</b> {a.appointment_time}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default AppointmentPage;
