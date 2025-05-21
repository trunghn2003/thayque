import React, { useEffect, useState } from "react";
import DoctorScheduleSelect from "./DoctorScheduleSelect";

function AppointmentPage() {
  const [appointments, setAppointments] = useState([]);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [slotId, setSlotId] = useState("");
  const [reason, setReason] = useState("");
  const userType = localStorage.getItem('user_type');

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

  const handleSubmit = async e => {
    e.preventDefault();
    setError(""); setSuccess("");
    if (!slotId) { setError("Bạn phải chọn bác sĩ và thời gian!"); return; }
    try {
      const res = await fetch("http://localhost:8001/api/appointments/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + localStorage.getItem("token")
        },
        body: JSON.stringify({ schedule_slot: slotId, reason })
      });
      if (res.status === 201) {
        setSuccess("Đặt lịch thành công!");
        setSlotId(""); setReason("");
        fetchAppointments();
      } else {
        const data = await res.json();
        setError(data.detail || "Đặt lịch thất bại");
      }
    } catch {
      setError("Lỗi kết nối appointment_service");
    }
  };

  return (
    <div>
      <h2>Danh sách lịch hẹn</h2>
      {error && <div style={{color: 'red'}}>{error}</div>}
      {success && <div style={{color: 'green'}}>{success}</div>}
      {userType === 'patient' && (
        <form onSubmit={handleSubmit} style={{marginBottom: 24, background: '#f8f8f8', padding: 16, borderRadius: 8}}>
          <h4>Đặt lịch hẹn mới</h4>
          <DoctorScheduleSelect onSelect={setSlotId} />{' '}
          <input value={reason} onChange={e => setReason(e.target.value)} placeholder="Lý do khám" required style={{width: 200, marginLeft: 8}} />{' '}
          <button type="submit">Đặt lịch</button>
        </form>
      )}
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
