import React, { useEffect, useState } from "react";

function PatientRecordPage() {
  const [record, setRecord] = useState(null);
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    full_name: "",
    date_of_birth: "",
    gender: "",
    address: "",
    phone: ""
  });
  const [editing, setEditing] = useState(false);
  const userType = localStorage.getItem('user_type');

  const fetchMyRecord = async () => {
    setError("");
    try {
      const res = await fetch("http://localhost:8002/api/patients/me/", {
        headers: { "Authorization": "Bearer " + localStorage.getItem("token") }
      });
      if (res.status === 404) {
        setRecord(null);
      } else {
        const data = await res.json();
        if (res.status === 200) {
          setRecord(data);
          setForm({
            full_name: data.full_name,
            date_of_birth: data.date_of_birth,
            gender: data.gender,
            address: data.address,
            phone: data.phone
          });
        } else setError("Không lấy được hồ sơ bệnh án");
      }
    } catch {
      setError("Lỗi kết nối patient_service");
    }
  };

  useEffect(() => {
    if (userType === 'patient') fetchMyRecord();
  }, [userType]);

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setError("");
    try {
      let res;
      if (record) {
        res = await fetch(`http://localhost:8002/api/patients/${record.id}/`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + localStorage.getItem("token")
          },
          body: JSON.stringify(form)
        });
      } else {
        res = await fetch("http://localhost:8002/api/patients/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + localStorage.getItem("token")
          },
          body: JSON.stringify(form)
        });
      }
      if (res.status === 200 || res.status === 201) {
        setEditing(false);
        fetchMyRecord();
      } else {
        setError("Lưu hồ sơ thất bại");
      }
    } catch {
      setError("Lỗi kết nối patient_service");
    }
  };

  if (userType !== 'patient') {
    return null;
  }

  return (
    <div>
      <h2>Hồ sơ bệnh án của tôi</h2>
      {error && <div style={{color: 'red'}}>{error}</div>}
      {record && !editing ? (
        <div style={{background: '#f8f8f8', padding: 16, borderRadius: 8, marginBottom: 16}}>
          <b>{record.full_name}</b> - Ngày sinh: {record.date_of_birth} - Giới tính: {record.gender} - Địa chỉ: {record.address} - SĐT: {record.phone}
          <button style={{marginLeft: 8}} onClick={() => setEditing(true)}>Sửa</button>
        </div>
      ) : (
        <form onSubmit={handleSubmit} style={{marginBottom: 20, background: '#f8f8f8', padding: 16, borderRadius: 8}}>
          <h4>{record ? "Cập nhật hồ sơ" : "Tạo hồ sơ bệnh án của bạn"}</h4>
          <input name="full_name" placeholder="Họ tên" value={form.full_name} onChange={handleChange} required />{' '}
          <input name="date_of_birth" type="date" placeholder="Ngày sinh" value={form.date_of_birth} onChange={handleChange} required />{' '}
          <select name="gender" value={form.gender} onChange={handleChange} required>
            <option value="">Giới tính</option>
            <option value="male">Nam</option>
            <option value="female">Nữ</option>
            <option value="other">Khác</option>
          </select>{' '}
          <input name="address" placeholder="Địa chỉ" value={form.address} onChange={handleChange} required />{' '}
          <input name="phone" placeholder="SĐT" value={form.phone} onChange={handleChange} required />{' '}
          <button type="submit">{record ? "Lưu" : "Tạo mới"}</button>
          {record && <button type="button" onClick={() => setEditing(false)}>Hủy</button>}
        </form>
      )}
    </div>
  );
}

export default PatientRecordPage;
