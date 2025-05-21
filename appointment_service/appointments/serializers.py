from rest_framework import serializers
from .models import Appointment, DoctorSchedule

class DoctorScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSchedule
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ('appointment_time',)
        extra_kwargs = {
            'appointment_time': {'required': False, 'allow_null': True}
        }

