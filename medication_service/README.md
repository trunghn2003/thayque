# Medication Service - Hướng dẫn sử dụng

## 1. Khởi động service

```bash
cd medication_service
python manage.py migrate
python manage.py runserver 8003
```

## 2. Seed dữ liệu mẫu

```bash
python manage.py shell < medications/seed.py
```

## 3. Các luồng nghiệp vụ chính

- **Lấy danh sách thuốc:**
  - GET `/api/medications/`
- **Lấy danh sách chẩn đoán (diagnosis) theo patient_record:**
  - GET `/api/diagnoses/?patient_record=<id>`
- **Lấy đơn thuốc theo diagnosis:**
  - GET `/api/prescriptions/?diagnosis=<diagnosis_id>`
- **Lấy xét nghiệm theo diagnosis:**
  - GET `/api/lab-tests/?diagnosis=<diagnosis_id>`
- **Tạo mới đơn thuốc, xét nghiệm, chẩn đoán:**
  - POST các endpoint tương ứng, tham khảo file Postman collection

## 4. Luồng tổng thể (tích hợp frontend)

1. Đăng nhập bằng tài khoản bệnh nhân hoặc bác sĩ để lấy JWT token.
2. Bệnh nhân xem lịch sử khám/đơn thuốc/xét nghiệm tại trang "Lịch sử khám/đơn thuốc" trên frontend.
3. Bác sĩ lưu kết quả khám, kê đơn, tạo xét nghiệm qua API hoặc giao diện frontend (nếu có).
4. Hệ thống tự động sinh nhắc nhở uống thuốc, tái khám dựa trên Prescription và Appointment.

## 5. Tham khảo thêm
- File Postman: `medication_service_api_test.postman_collection.json`
- Các API đều yêu cầu header: `Authorization: Bearer <token>`

## 6. Lưu ý
- Đảm bảo đã seed user, patient_record, appointment phù hợp ở các service liên quan.
- Nếu gặp lỗi liên quan đến trường `patient_id`, hãy kiểm tra lại migration/model và khởi động lại service.
