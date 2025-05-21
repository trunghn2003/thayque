import React, { useEffect, useState } from "react";

function ReminderPage() {
  const [reminders, setReminders] = useState([]);
  const [error, setError] = useState("");

  const fetchReminders = async () => {
    setError("");
    try {
      const res = await fetch("http://localhost:8003/api/reminders/", {
        headers: { "Authorization": "Bearer " + localStorage.getItem("token") }
      });
      const data = await res.json();
      if (res.status === 200) setReminders(data);
      else setError("Không lấy được danh sách nhắc nhở");
    } catch {
      setError("Lỗi kết nối medication_service");
    }
  };

  useEffect(() => {
    fetchReminders();
  }, []);

  const handleDelete = async id => {
    if (!window.confirm("Xóa nhắc nhở này?")) return;
    setError("");
    try {
      const res = await fetch(`http://localhost:8003/api/reminders/${id}/`, {
        method: "DELETE",
        headers: { "Authorization": "Bearer " + localStorage.getItem("token") }
      });
      if (res.status === 204) fetchReminders();
      else setError("Xóa nhắc nhở thất bại");
    } catch {
      setError("Lỗi kết nối medication_service");
    }
  };

  return (
    <div>
      <h2>Danh sách nhắc nhở</h2>
      {error && <div style={{color: 'red'}}>{error}</div>}
      <ul>
        {reminders.length === 0 && <li>Không có nhắc nhở nào.</li>}
        {reminders.map(r => (
          <li key={r.id} style={{marginBottom: 8}}>
            <b>{r.title || r.type}</b> - {r.message} <br/>
            Thời gian: {r.remind_time} {r.related_type && `(Loại: ${r.related_type})`}
            <button style={{marginLeft: 8}} onClick={() => handleDelete(r.id)}>Xóa</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ReminderPage;
