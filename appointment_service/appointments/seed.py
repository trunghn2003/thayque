import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
import random
import requests
from datetime import datetime, timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appointment_service.settings')
django.setup()

from appointments.models import DoctorSchedule, Appointment

# Danh sách bác sĩ mẫu (username, tên, id cố định)
doctors = [
    {'username': 'doctor1', 'name': 'Dr. Nguyễn Văn A', 'id': 3},
    {'username': 'doctor2', 'name': 'Dr. Trần Thị B', 'id': 4},
    {'username': 'doctor3', 'name': 'Dr. Lê Văn C', 'id': 5},
]

# Tạo lịch làm việc cho mỗi bác sĩ trong 7 ngày tới, mỗi ngày 2 slot
now = timezone.now()
schedule_objs = []
for d in doctors:
    for i in range(7):
        day = now + timedelta(days=i)
        for slot in [(8, 0), (14, 0)]:
            start = day.replace(hour=slot[0], minute=slot[1], second=0, microsecond=0)
            end = start + timedelta(hours=1)
            start = timezone.make_aware(start) if timezone.is_naive(start) else start
            end = timezone.make_aware(end) if timezone.is_naive(end) else end
            obj, created = DoctorSchedule.objects.get_or_create(
                doctor_id=d['id'],
                start_time=start,
                end_time=end,
                defaults={'is_available': True}
            )
            schedule_objs.append(obj)
print(f"Đã tạo {len(schedule_objs)} slot lịch làm việc cho {len(doctors)} bác sĩ.")

# (Tuỳ chọn) Tạo một số lịch hẹn mẫu cho bệnh nhân id=5
for i in range(3):
    slot = random.choice(schedule_objs)
    appt_time = slot.start_time
    Appointment.objects.get_or_create(
        patient_id=5,
        doctor_id=slot.doctor_id,
        schedule_slot=slot,
        appointment_time=appt_time,
        reason=f"Khám định kỳ lần {i+1}",
        status='Scheduled'
    )
print("Đã tạo một số lịch hẹn mẫu cho bệnh nhân id=5.")
