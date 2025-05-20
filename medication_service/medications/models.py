from django.db import models

# Create your models here.
class Medication(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=20, blank=True)  # Đơn vị (viên, lọ, v.v.)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Diagnosis(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    appointment = models.IntegerField(null=True, blank=True, help_text="ID of Appointment from appointment_service")
    patient_record = models.IntegerField(null=True, blank=True, help_text="ID of PatientRecord from patient_service")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Prescription(models.Model):
    diagnosis = models.ForeignKey(Diagnosis, related_name='prescriptions', on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, related_name='prescriptions', on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    instructions = models.TextField(blank=True)
    appointment = models.IntegerField(null=True, blank=True, help_text="ID of Appointment from appointment_service")
    patient_record = models.IntegerField(null=True, blank=True, help_text="ID of PatientRecord from patient_service")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.medication.name} ({self.dosage}) for {self.diagnosis.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Tự động tạo nhắc nhở uống thuốc khi tạo mới Prescription
        if self.pk and self.medication and self.patient_record and self.appointment:
            from .models import Reminder
            # Kiểm tra đã có reminder cho prescription này chưa
            if not Reminder.objects.filter(prescription=self).exists():
                Reminder.objects.create(
                    patient_id=None,  # Có thể lấy từ patient_record nếu cần mapping
                    patient_record=self.patient_record,
                    appointment=self.appointment,
                    prescription=self,
                    medication=self.medication,
                    message=f"Nhắc uống thuốc {self.medication.name}: {self.dosage}",
                    remind_time=None,  # Có thể tính toán từ instructions hoặc truyền vào
                    type="medication",
                    quantity=None  # Có thể parse từ dosage nếu cần
                )

class LabTest(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    diagnosis = models.ForeignKey(Diagnosis, related_name='lab_tests', on_delete=models.CASCADE, null=True, blank=True)
    appointment = models.IntegerField(null=True, blank=True, help_text="ID of Appointment from appointment_service")
    patient_record = models.IntegerField(null=True, blank=True, help_text="ID of PatientRecord from patient_service")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Reminder(models.Model):
    patient_id = models.IntegerField()
    patient_record = models.IntegerField(null=True, blank=True)
    appointment = models.IntegerField(null=True, blank=True)
    prescription = models.ForeignKey('Prescription', null=True, blank=True, on_delete=models.SET_NULL)
    medication = models.ForeignKey('Medication', null=True, blank=True, on_delete=models.SET_NULL)
    message = models.CharField(max_length=255)
    remind_time = models.DateTimeField()
    type = models.CharField(max_length=50, default="general")  # 'medication', 'appointment', ...
    quantity = models.PositiveIntegerField(null=True, blank=True)
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reminder for patient {self.patient_id} at {self.remind_time}"
