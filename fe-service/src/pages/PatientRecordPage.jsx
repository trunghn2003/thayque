import React, { useEffect, useState } from "react";

function PatientRecordPage() {
  const [records, setRecords] = useState([]);
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    full_name: "",
    date_of_birth: "",
    gender: "",
    address: "",
    phone: ""
  });
  const [editingId, setEditingId] = useState(null);

  const fetchRecords = async () => {
    setError("");
    try {
      const res = await fetch("http://localhost:8002/api/patients/", {
        headers: { "Authorization": "Bearer " + localStorage.getItem("token") }
      });
      const data = await res.json();
      if (res.status === 200) setRecords(data);
      else setError("Không lấy được hồ sơ bệnh án");
    } catch {
      setError("Lỗi kết nối patient_service");
    }
  };

  useEffect(() => {
    fetchRecords();
  }, []);

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setError("");
    const method = editingId ? "PUT" : "POST";
    const url = editingId
      ? `http://localhost:8002/api/patients/${editingId}/`
      : "http://localhost:8002/api/patients/";
    try {
      const res = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + localStorage.getItem("token")
        },
        body: JSON.stringify(form)
      });
      if (res.status === 200 || res.status === 201) {
        setForm({ full_name: "", date_of_birth: "", gender: "", address: "", phone: "" });
        setEditingId(null);
        fetchRecords();
      } else {
        setError("Lưu hồ sơ thất bại");
      }
    } catch {
      setError("Lỗi kết nối patient_service");
    }
  };

  const handleDelete = async id => {
    if (!window.confirm("Xóa hồ sơ này?")) return;
    setError("");
    try {
      const res = await fetch(`http://localhost:8002/api/patients/${id}/`, {
        method: "DELETE",
        headers: { "Authorization": "Bearer " + localStorage.getItem("token") }
      });
      if (res.status === 204) fetchRecords();
      else setError("Xóa hồ sơ thất bại");
    } catch {
      setError("Lỗi kết nối patient_service");
    }
  };

  const handleEdit = record => {
    setForm({
      full_name: record.full_name,
      date_of_birth: record.date_of_birth,
      gender: record.gender,
      address: record.address,
      phone: record.phone
    });
    setEditingId(record.id);
  };

  const handleCancelEdit = () => {
    setForm({ full_name: "", date_of_birth: "", gender: "", address: "", phone: "" });
    setEditingId(null);
  };

  return (
    <div>
      <h2>Hồ sơ bệnh án</h2>
      {error && <div style={{color: 'red'}}>{error}</div>}
      <form onSubmit={handleSubmit} style={{marginBottom: 20, background: '#f8f8f8', padding: 16, borderRadius: 8}}>
        <h4>{editingId ? "Cập nhật hồ sơ" : "Thêm mới hồ sơ"}</h4>
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
        <button type="submit">{editingId ? "Lưu" : "Thêm"}</button>
        {editingId && <button type="button" onClick={handleCancelEdit}>Hủy</button>}
      </form>
      <ul>
        {records.map(r => (
          <li key={r.id} style={{marginBottom: 8}}>
            <b>{r.full_name}</b> - Ngày sinh: {r.date_of_birth} - Giới tính: {r.gender} - Địa chỉ: {r.address} - SĐT: {r.phone}
            <button style={{marginLeft: 8}} onClick={() => handleEdit(r)}>Sửa</button>
            <button style={{marginLeft: 4}} onClick={() => handleDelete(r.id)}>Xóa</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default PatientRecordPage;
