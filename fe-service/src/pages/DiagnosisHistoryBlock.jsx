import React, { useEffect, useState } from "react";

export default function DiagnosisHistoryBlock({ diagnosis }) {
  const [prescriptions, setPrescriptions] = useState([]);
  const [labtests, setLabtests] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchDetails = async () => {
      setError("");
      try {
        const presRes = await fetch(`http://localhost:8003/api/prescriptions/?diagnosis=${diagnosis.id}`, {
          headers: { "Authorization": "Bearer " + localStorage.getItem("token") }
        });
        const presData = await presRes.json();
        if (presRes.status === 200) setPrescriptions(presData);
        else setError("Không lấy được đơn thuốc");
        const labRes = await fetch(`http://localhost:8003/api/lab-tests/?diagnosis=${diagnosis.id}`, {
          headers: { "Authorization": "Bearer " + localStorage.getItem("token") }
        });
        const labData = await labRes.json();
        if (labRes.status === 200) setLabtests(labData);
        else setError("Không lấy được xét nghiệm");
      } catch {
        setError("Lỗi kết nối medication_service");
      }
    };
    fetchDetails();
  }, [diagnosis.id]);

  return (
    <div style={{border: '1px solid #ccc', borderRadius: 8, marginBottom: 16, padding: 16, background: '#f9f9f9'}}>
      <div><b>Ngày khám:</b> {new Date(diagnosis.created_at).toLocaleString()} | <b>Kết luận:</b> {diagnosis.name}</div>
      {diagnosis.description && <div><b>Mô tả:</b> {diagnosis.description}</div>}
      <div style={{marginTop: 8}}>
        <b>Đơn thuốc:</b>
        {prescriptions.length === 0 ? <span> Không có.</span> :
          <ul style={{margin: 0, paddingLeft: 20}}>
            {prescriptions.map(p => (
              <li key={p.id}>
                <b>Thuốc:</b> {p.medication} | <b>Liều dùng:</b> {p.dosage} | <b>Hướng dẫn:</b> {p.instructions}
              </li>
            ))}
          </ul>
        }
      </div>
      <div style={{marginTop: 8}}>
        <b>Xét nghiệm:</b>
        {labtests.length === 0 ? <span> Không có.</span> :
          <ul style={{margin: 0, paddingLeft: 20}}>
            {labtests.map(l => (
              <li key={l.id}>
                <b>Tên:</b> {l.name} | <b>Mô tả:</b> {l.description}
              </li>
            ))}
          </ul>
        }
      </div>
      {error && <div style={{color:'red'}}>{error}</div>}
    </div>
  );
}
