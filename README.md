# Microservice Healthcare System

## Tổng quan
Hệ thống gồm 4 microservice chính, mỗi service là một Django project độc lập:
- **user_service**: Đăng ký, đăng nhập, phân quyền user (patient, doctor, admin).
- **appointment_service**: Đặt lịch hẹn, quản lý lịch làm việc bác sĩ, quản lý lịch hẹn khám bệnh.
- **patient_service**: Quản lý hồ sơ bệnh nhân.
- **medication_service**: Quản lý thuốc, chẩn đoán, đơn thuốc, xét nghiệm.

## Cổng dịch vụ (Port)
- user_service:           http://localhost:8004/
- appointment_service:    http://localhost:8001/
- patient_service:        http://localhost:8002/
- medication_service:     http://localhost:8003/

## Luồng hoạt động tổng thể
1. **User đăng ký/đăng nhập** qua user_service, nhận JWT token và phân quyền.
2. **Bệnh nhân đặt lịch hẹn** qua appointment_service (chọn bác sĩ, thời gian, lý do).
3. **Hệ thống kiểm tra lịch làm việc bác sĩ** (DoctorSchedule) và các slot còn trống.
4. **Tạo Appointment** nếu hợp lệ, trạng thái Scheduled.
5. **Bác sĩ xác nhận/hoàn thành lịch hẹn** (Confirmed/Completed).
6. **Bác sĩ cập nhật chẩn đoán, xét nghiệm, kê đơn thuốc** (Prescription, LabTest) cho lịch hẹn.
7. **Đơn thuốc** liên kết với thuốc từ medication_service.
8. **Hồ sơ bệnh nhân** quản lý độc lập qua patient_service, liên kết lịch sử khám qua patient_id.

## Khởi động tất cả service
```sh
chmod +x run_all_services.sh
./run_all_services.sh
```

## Cài đặt thư viện cho từng service
```sh
cd <service_folder>
pip install -r requirements.txt
```

## Test API
Import các file *.postman_collection.json vào Postman để test từng service.

## Scripts lưu token (ví dụ với user_service)
Sau khi đăng nhập thành công, bạn có thể lưu token vào file bằng script bash:
```sh
curl -X POST http://localhost:8004/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "TestPassword123"}' \
  | jq -r '.access' > user_token.txt
```

## Liên hệ
- Mọi thắc mắc hoặc cần mở rộng, vui lòng liên hệ nhóm phát triển.
