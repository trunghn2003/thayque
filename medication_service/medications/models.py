from django.db import models
from datetime import datetime, timedelta, time

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
        is_new = self.pk is None
        super().save(*args, **kwargs)
        # Tự động tạo nhắc nhở uống thuốc khi tạo mới Prescription
        if is_new and self.medication and self.patient_record and self.appointment:
            from .models import Reminder
            # Ví dụ: parse dosage/instructions để xác định các mốc giờ uống thuốc
            # Ở đây giả sử nếu 'sáng' trong instructions thì 7:00, 'tối' thì 19:00
            times = []
            instr = (self.instructions or '').lower() + ' ' + (self.dosage or '').lower()
            if 'sáng' in instr:
                times.append(time(7, 0))
            if 'trưa' in instr:
                times.append(time(12, 0))
            if 'chiều' in instr:
                times.append(time(17, 0))
            if 'tối' in instr:
                times.append(time(19, 0))
            if not times:
                times = [time(7, 0)]  # Mặc định 1 lần buổi sáng nếu không rõ
            today = datetime.now().date()
            for t in times:
                remind_dt = datetime.combine(today, t)
                Reminder.objects.create(
                    patient_id=None,
                    patient_record=self.patient_record,
                    appointment=self.appointment,
                    prescription=self,
                    medication=self.medication,
                    message=f"Nhắc uống thuốc {self.medication.name}: {self.dosage}",
                    remind_time=remind_dt,
                    type="medication",
                    quantity=None
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

class Appointment(models.Model):
    # ...existing fields...
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        # Tự động tạo nhắc nhở tái khám trước 3 ngày
        if is_new and self.patient_id and self.doctor_id and self.appointment_time:
            from medications.models import Reminder
            remind_dt = self.appointment_time - timedelta(days=3)
            Reminder.objects.create(
                patient_id=self.patient_id,
                patient_record=None,
                appointment=self.id,
                prescription=None,
                medication=None,
                message="Nhắc lịch tái khám trong 3 ngày tới!",
                remind_time=remind_dt,
                type="appointment",
                quantity=None
            )
