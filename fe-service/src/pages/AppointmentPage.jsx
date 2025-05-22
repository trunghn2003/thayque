import React, { useEffect, useState } from "react";
import DoctorScheduleSelect from "./DoctorScheduleSelect";
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';

function AppointmentPage() {
  const [appointments, setAppointments] = useState([]);
  const [schedules, setSchedules] = useState([]); // Lịch làm việc của bác sĩ
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [slotId, setSlotId] = useState("");
  const [reason, setReason] = useState("");
  const [doctorId, setDoctorId] = useState(""); // Add doctorId state
  const [newSchedule, setNewSchedule] = useState({
    date: "",
    start_time: "",
    end_time: "",
    doctor_id: "" // Add doctor_id field
  });
  
  const userType = localStorage.getItem('user_type');

  useEffect(() => {
    // Get doctor_id from localStorage when component mounts
    if (userType === 'doctor') {
      const userId = localStorage.getItem('user_id');
      setDoctorId(userId);
      setNewSchedule(prev => ({ ...prev, doctor_id: userId }));
    }
  }, [userType]);

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

  const fetchDoctorSchedules = async () => {
    if (userType !== 'doctor') return;
    try {
      const res = await fetch("http://localhost:8001/api/doctor-schedules/", {
        headers: { "Authorization": "Bearer " + localStorage.getItem("token") }
      });
      const data = await res.json();
      if (res.status === 200) setSchedules(data);
      else setError("Không lấy được lịch làm việc");
    } catch {
      setError("Lỗi kết nối khi lấy lịch làm việc");
    }
  };

  const fetchDoctorInfo = async () => {
    if (userType !== 'doctor') return;
    try {
      const res = await fetch("http://localhost:8000/api/users/me/", {
        headers: { "Authorization": "Bearer " + localStorage.getItem("token") }
      });
      const data = await res.json();
      if (res.status === 200) {
        setDoctorId(data.id);
        setNewSchedule(prev => ({ ...prev, doctor_id: data.id }));
      } else {
        setError("Không lấy được thông tin bác sĩ");
      }
    } catch {
      setError("Lỗi kết nối khi lấy thông tin bác sĩ");
    }
  };

  useEffect(() => {
    fetchAppointments();
    fetchDoctorInfo();
    fetchDoctorSchedules();
  }, [userType]);

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

  const handleAddSchedule = async (e) => {
    e.preventDefault();
    setError(""); setSuccess("");
    if (!doctorId) {
      setError("Không thể xác định ID bác sĩ!");
      return;
    }
    try {
      const res = await fetch("http://localhost:8001/api/doctor-schedules/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + localStorage.getItem("token")
        },
        body: JSON.stringify({ ...newSchedule, doctor_id: doctorId })
      });
      if (res.status === 201) {
        setSuccess("Thêm lịch làm việc thành công!");
        setNewSchedule({ date: "", start_time: "", end_time: "" });
        fetchDoctorSchedules();
      } else {
        const data = await res.json();
        setError(data.detail || "Thêm lịch làm việc thất bại");
      }
    } catch {
      setError("Lỗi kết nối khi thêm lịch làm việc");
    }
  };

  // Convert appointments and schedules to FullCalendar events
  const getCalendarEvents = () => {
    const events = [];
    
    // Add doctor schedules
    if (userType === 'doctor') {
      schedules.forEach(schedule => {
        events.push({
          id: `schedule-${schedule.id}`,
          title: 'Lịch làm việc',
          start: `${schedule.date}T${schedule.start_time}`,
          end: `${schedule.date}T${schedule.end_time}`,
          backgroundColor: '#2196f3',
          extendedProps: {
            type: 'schedule',
            scheduleId: schedule.id
          }
        });
      });
    }

    // Add appointments
    appointments.forEach(appointment => {
      const color = appointment.status === 'pending' ? '#ff9800' :
                   appointment.status === 'Confirmed' ? '#4caf50' :
                   appointment.status === 'Completed' ? '#9e9e9e' :
                   appointment.status === 'Cancelled' ? '#f44336' : '#2196f3';
                   
      const title = userType === 'doctor' ? 
                   `Lịch hẹn - BN:${appointment.patient_id}` :
                   `Lịch hẹn - BS:${appointment.doctor_id}`;

      events.push({
        id: `appointment-${appointment.id}`,
        title: title,
        start: new Date(appointment.appointment_time),
        backgroundColor: color,
        extendedProps: {
          type: 'appointment',
          appointmentId: appointment.id,
          status: appointment.status,
          reason: appointment.reason
        }
      });
    });

    return events;
  };

  const handleUpdateAppointment = async (appointmentId, status) => {
    setError(""); setSuccess("");
    try {
      const res = await fetch(`http://localhost:8001/api/appointments/${appointmentId}/`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + localStorage.getItem("token")
        },
        body: JSON.stringify({ status })
      });
      if (res.status === 200) {
        const statusMessages = {
          'Confirmed': 'Đã xác nhận lịch hẹn thành công!',
          'Cancelled': 'Đã từ chối lịch hẹn.',
          'Completed': 'Đã đánh dấu lịch hẹn hoàn thành.',
        };
        setSuccess(statusMessages[status] || 'Cập nhật trạng thái lịch hẹn thành công!');
        fetchAppointments();
      } else {
        const data = await res.json();
        setError(data.detail || "Cập nhật trạng thái lịch hẹn thất bại");
      }
    } catch {
      setError("Lỗi kết nối khi cập nhật lịch hẹn");
    }
  };

  // Group appointments by status
  const appointmentsByStatus = appointments.reduce((acc, appointment) => {
    const status = appointment.status || 'pending';
    if (!acc[status]) acc[status] = [];
    acc[status].push(appointment);
    return acc;
  }, {});

  // Format datetime for display
  const formatDateTime = (dateTimeStr) => {
    return new Date(dateTimeStr).toLocaleString('vi-VN', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div>
      <h2>Quản lý lịch hẹn {userType === 'doctor' ? 'của bác sĩ' : ''}</h2>
      {error && <div style={{color: 'red'}}>{error}</div>}
      {success && <div style={{color: 'green'}}>{success}</div>}

      {/* Calendar View */}
      <div style={{ marginBottom: 24, height: '600px' }}>
        <FullCalendar
          plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
          initialView="timeGridWeek"
          headerToolbar={{
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
          }}
          events={getCalendarEvents()}
          slotMinTime="08:00:00"
          slotMaxTime="18:00:00"
          allDaySlot={false}
          locale="vi"
          eventClick={info => {
            const event = info.event;
            const { type, appointmentId, status, reason } = event.extendedProps;
            
            if (type === 'appointment' && userType === 'doctor') {
              // Show modal or prompt for appointment actions
              if (status === 'pending') {
                const action = window.confirm(
                  `Lịch hẹn: ${reason || 'Không có lý do'}\n\nBạn muốn xác nhận lịch hẹn này?`
                );
                if (action !== null) {
                  handleUpdateAppointment(appointmentId, action ? 'Confirmed' : 'Cancelled');
                }
              } else if (status === 'Confirmed') {
                if (window.confirm('Đánh dấu lịch hẹn này là đã hoàn thành?')) {
                  handleUpdateAppointment(appointmentId, 'Completed');
                }
              }
            }
          }}
          eventContent={info => {
            return (
              <div style={{ fontSize: '0.8em', padding: '2px' }}>
                <div style={{ fontWeight: 'bold' }}>{info.event.title}</div>
                {info.event.extendedProps.reason && (
                  <div>{info.event.extendedProps.reason}</div>
                )}
                {info.event.extendedProps.type === 'appointment' && (
                  <div style={{ fontStyle: 'italic' }}>
                    {info.event.extendedProps.status === 'pending' ? 'Chờ xác nhận' :
                     info.event.extendedProps.status === 'Confirmed' ? 'Đã xác nhận' :
                     info.event.extendedProps.status === 'Completed' ? 'Đã hoàn thành' :
                     'Đã hủy'}
                  </div>
                )}
              </div>
            );
          }}
        />
      </div>

      {/* Form thêm lịch làm việc cho bác sĩ */}
      {userType === 'doctor' && (
        <div style={{marginBottom: 24}}>
          <h3>Thêm lịch làm việc mới</h3>
          <form onSubmit={handleAddSchedule} style={{background: '#f8f8f8', padding: 16, borderRadius: 8}}>
            <div style={{marginBottom: 8}}>
              <label style={{marginRight: 8}}>Ngày:</label>
              <input
                type="date"
                value={newSchedule.date}
                onChange={e => setNewSchedule({...newSchedule, date: e.target.value})}
                required
              />
            </div>
            <div style={{marginBottom: 8}}>
              <label style={{marginRight: 8}}>Giờ bắt đầu:</label>
              <input
                type="time"
                value={newSchedule.start_time}
                onChange={e => setNewSchedule({...newSchedule, start_time: e.target.value})}
                required
              />
            </div>
            <div style={{marginBottom: 8}}>
              <label style={{marginRight: 8}}>Giờ kết thúc:</label>
              <input
                type="time"
                value={newSchedule.end_time}
                onChange={e => setNewSchedule({...newSchedule, end_time: e.target.value})}
                required
              />
            </div>
            <button type="submit" style={{backgroundColor: '#4CAF50', color: 'white', padding: '8px 16px', border: 'none', borderRadius: 4, cursor: 'pointer'}}>
              Thêm lịch
            </button>
          </form>
        </div>
      )}

      {/* Form đặt lịch cho bệnh nhân */}
      {userType === 'patient' && (
        <form onSubmit={handleSubmit} style={{marginBottom: 24, background: '#f8f8f8', padding: 16, borderRadius: 8}}>
          <h4>Đặt lịch hẹn mới</h4>
          <DoctorScheduleSelect onSelect={setSlotId} />
          <input 
            value={reason} 
            onChange={e => setReason(e.target.value)} 
            placeholder="Lý do khám" 
            required 
            style={{width: 200, marginLeft: 8}} 
          />
          <button 
            type="submit"
            style={{
              backgroundColor: '#4CAF50',
              color: 'white',
              padding: '8px 16px',
              border: 'none',
              borderRadius: 4,
              marginLeft: 8,
              cursor: 'pointer'
            }}
          >
            Đặt lịch
          </button>
        </form>
      )}

      {/* Chú thích màu sắc */}
      <div style={{marginTop: 24, background: '#f8f8f8', padding: 16, borderRadius: 8}}>
        <h4>Chú thích:</h4>
        <div style={{display: 'flex', gap: 16, flexWrap: 'wrap'}}>
          {userType === 'doctor' && (
            <div style={{display: 'flex', alignItems: 'center'}}>
              <div style={{width: 20, height: 20, backgroundColor: '#2196f3', marginRight: 8, borderRadius: 4}}></div>
              <span>Lịch làm việc</span>
            </div>
          )}
          <div style={{display: 'flex', alignItems: 'center'}}>
            <div style={{width: 20, height: 20, backgroundColor: '#ff9800', marginRight: 8, borderRadius: 4}}></div>
            <span>Chờ xác nhận</span>
          </div>
          <div style={{display: 'flex', alignItems: 'center'}}>
            <div style={{width: 20, height: 20, backgroundColor: '#4caf50', marginRight: 8, borderRadius: 4}}></div>
            <span>Đã xác nhận</span>
          </div>
          <div style={{display: 'flex', alignItems: 'center'}}>
            <div style={{width: 20, height: 20, backgroundColor: '#9e9e9e', marginRight: 8, borderRadius: 4}}></div>
            <span>Đã hoàn thành</span>
          </div>
          <div style={{display: 'flex', alignItems: 'center'}}>
            <div style={{width: 20, height: 20, backgroundColor: '#f44336', marginRight: 8, borderRadius: 4}}></div>
            <span>Đã hủy</span>
          </div>
        </div>
        <div style={{marginTop: 16}}>
          <p><strong>Hướng dẫn:</strong></p>
          <ul style={{margin: 0, paddingLeft: 20}}>
            <li>Click vào một lịch hẹn để xem chi tiết và cập nhật trạng thái</li>
            {userType === 'doctor' && (
              <li>Thêm lịch làm việc mới bằng form bên dưới</li>
            )}
            {userType === 'patient' && (
              <li>Đặt lịch hẹn mới bằng form bên trên</li>
            )}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default AppointmentPage;
