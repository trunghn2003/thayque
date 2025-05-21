from medications.models import Medication, Diagnosis, Prescription, LabTest
from django.utils import timezone

# Tạo thuốc mẫu
med1 = Medication.objects.create(name="Paracetamol", description="Thuốc giảm đau hạ sốt", unit="viên", quantity=100)
med2 = Medication.objects.create(name="Amoxicillin", description="Kháng sinh phổ rộng", unit="viên", quantity=50)

# Tạo một lần khám (diagnosis) mẫu
now = timezone.now()
diag1 = Diagnosis.objects.create(name="Cảm cúm", description="Sốt nhẹ, đau đầu", appointment=1, patient_record=1, created_at=now)

diag2 = Diagnosis.objects.create(name="Viêm họng", description="Đau họng, ho", appointment=2, patient_record=1, created_at=now)

# Đơn thuốc cho từng lần khám
Prescription.objects.create(diagnosis=diag1, medication=med1, dosage="2 viên/ngày", instructions="Uống sau ăn sáng và tối", appointment=1, patient_record=1)
Prescription.objects.create(diagnosis=diag2, medication=med2, dosage="1 viên/ngày", instructions="Uống sáng", appointment=2, patient_record=1)

# Xét nghiệm cho từng lần khám
LabTest.objects.create(name="Xét nghiệm máu", description="Kiểm tra công thức máu", diagnosis=diag1, appointment=1, patient_record=1)
LabTest.objects.create(name="Xét nghiệm nước tiểu", description="Kiểm tra chức năng thận", diagnosis=diag2, appointment=2, patient_record=1)

print("Đã seed dữ liệu mẫu cho medication_service!")
