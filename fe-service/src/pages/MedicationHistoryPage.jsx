import React, { useEffect, useState } from "react";

function MedicationHistoryPage() {
  const [medications, setMedications] = useState([]);
  const [error, setError] = useState("");

  const fetchMedications = async () => {
    setError("");
    try {
      const res = await fetch("http://localhost:8003/api/medications/", {
        headers: { "Authorization": "Bearer " + localStorage.getItem("token") }
      });
      const data = await res.json();
      if (res.status === 200) setMedications(data);
      else setError("Không lấy được lịch sử thuốc");
    } catch {
      setError("Lỗi kết nối medication_service");
    }
  };

  useEffect(() => {
    fetchMedications();
  }, []);

  return (
    <div>
      <h2>Lịch sử khám/đơn thuốc</h2>
      {error && <div style={{color: 'red'}}>{error}</div>}
      <ul>
        {medications.length === 0 && <li>Không có dữ liệu.</li>}
        {medications.map(m => (
          <li key={m.id} style={{marginBottom: 8}}>
            <b>Thuốc:</b> {m.name} | <b>Mô tả:</b> {m.description} | <b>Ngày tạo:</b> {m.created_at}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default MedicationHistoryPage;
