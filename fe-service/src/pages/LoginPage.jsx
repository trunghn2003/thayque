import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async e => {
    e.preventDefault();
    setError("");
    try {
      const res = await fetch("http://localhost:8004/api/users/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
      });
      const data = await res.json();
      if (res.status === 200 && data.access) {
        localStorage.setItem("token", data.access);
        localStorage.setItem("user_type", data.user_type);
        // Điều hướng theo role
        if (data.user_type === "doctor") navigate("/appointments");
        else navigate("/patient-records");
      } else {
        setError("Sai tài khoản hoặc mật khẩu");
      }
    } catch {
      setError("Lỗi kết nối user_service");
    }
  };

  return (
    <div style={{maxWidth: 400, margin: "40px auto", padding: 24, border: "1px solid #ccc", borderRadius: 8}}>
      <h2>Đăng nhập hệ thống</h2>
      {error && <div style={{color: 'red'}}>{error}</div>}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Tên đăng nhập"
          value={username}
          onChange={e => setUsername(e.target.value)}
          required
          style={{width: "100%", marginBottom: 12}}
        />
        <input
          type="password"
          placeholder="Mật khẩu"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
          style={{width: "100%", marginBottom: 12}}
        />
        <button type="submit" style={{width: "100%"}}>Đăng nhập</button>
      </form>
    </div>
  );
}

export default LoginPage;
