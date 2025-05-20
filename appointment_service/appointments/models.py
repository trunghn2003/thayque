from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings # Có thể cần nếu dùng AUTH_USER_MODEL, nhưng ở đây ta dùng ID

# Model Lịch làm việc của Bác sĩ
class DoctorSchedule(models.Model):
    doctor_id = models.IntegerField(
        _("doctor id"),
        db_index=True,
        help_text=_("ID of the Doctor from the User Service")
    )
    start_time = models.DateTimeField(_("start time"))
    end_time = models.DateTimeField(_("end time"))
    is_available = models.BooleanField(
        _("is available"),
        default=True,
        help_text=_("Is this time slot generally available (before considering appointments)?")
    )
    class Meta:
        verbose_name = _('doctor schedule')
        verbose_name_plural = _('doctor schedules')
        ordering = ['doctor_id', 'start_time']
    def __str__(self):
        return f"Dr. ID {self.doctor_id}: {self.start_time.strftime('%Y-%m-%d %H:%M')} - {self.end_time.strftime('%H:%M')}"

# Model Lịch hẹn khám bệnh
class Appointment(models.Model):
    STATUS_SCHEDULED = 'Scheduled'
    STATUS_CONFIRMED = 'Confirmed'
    STATUS_CANCELLED = 'Cancelled'
    STATUS_COMPLETED = 'Completed'
    STATUS_CHOICES = [
        (STATUS_SCHEDULED, _('Scheduled')),
        (STATUS_CONFIRMED, _('Confirmed')),
        (STATUS_CANCELLED, _('Cancelled')),
        (STATUS_COMPLETED, _('Completed')),
    ]
    patient_id = models.IntegerField(
        _("patient id"),
        db_index=True,
        help_text=_("ID of the Patient from the User Service")
    )
    doctor_id = models.IntegerField(
        _("doctor id"),
        db_index=True,
        help_text=_("ID of the Doctor from the User Service")
    )
    schedule_slot = models.ForeignKey(
        DoctorSchedule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointments',
        verbose_name=_("schedule slot")
    )
    appointment_time = models.DateTimeField(
        _("appointment time"),
        db_index=True
    )
    reason = models.TextField(
        _("reason for appointment"),
        blank=True,
        null=True
    )
    status = models.CharField(
        _("status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_SCHEDULED,
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = _('appointment')
        verbose_name_plural = _('appointments')
        unique_together = (('patient_id', 'appointment_time'), ('doctor_id', 'appointment_time'))
        ordering = ['appointment_time']
    def __str__(self):
        return f"Appt ID: {self.id} - Patient: {self.patient_id} with Dr: {self.doctor_id} at {self.appointment_time.strftime('%Y-%m-%d %H:%M')}"
