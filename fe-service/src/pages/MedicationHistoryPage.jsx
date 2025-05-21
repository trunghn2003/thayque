import React, { useEffect, useState } from "react";
import DiagnosisHistoryBlock from "./DiagnosisHistoryBlock";

function MedicationHistoryPage() {
  const [diagnoses, setDiagnoses] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      setError(""); setLoading(true);
      try {
        // Lấy patient_record của user hiện tại
        const recRes = await fetch("http://localhost:8002/api/patients/me/", {
          headers: { "Authorization": "Bearer " + localStorage.getItem("token") }
        });
        if (recRes.status !== 200) { setError("Không lấy được hồ sơ bệnh án"); setLoading(false); return; }
        const recData = await recRes.json();
        // Lấy danh sách các lần khám (diagnosis) theo patient_record
        const diagRes = await fetch(`http://localhost:8003/api/diagnoses/?patient_record=${recData.id}`, {
          headers: { "Authorization": "Bearer " + localStorage.getItem("token") }
        });
        const diagData = await diagRes.json();
        if (diagRes.status === 200) setDiagnoses(diagData);
        else setError("Không lấy được lịch sử khám");
      } catch {
        setError("Lỗi kết nối dịch vụ");
      }
      setLoading(false);
    };
    fetchHistory();
  }, []);

  return (
    <div>
      <h2>Lịch sử khám/đơn thuốc</h2>
      {error && <div style={{color: 'red'}}>{error}</div>}
      {loading ? <div>Đang tải...</div> :
        diagnoses.length === 0 ? <div>Không có dữ liệu.</div> :
        diagnoses.map(d => <DiagnosisHistoryBlock key={d.id} diagnosis={d} />)
      }
    </div>
  );
}

export default MedicationHistoryPage;
