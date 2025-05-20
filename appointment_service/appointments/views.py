from django.shortcuts import render
from rest_framework import viewsets
from .models import Appointment, DoctorSchedule
from .serializers import AppointmentSerializer, DoctorScheduleSerializer

# Create your views here.

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all().order_by('-created_at')
    serializer_class = AppointmentSerializer

class DoctorScheduleViewSet(viewsets.ModelViewSet):
    queryset = DoctorSchedule.objects.all().order_by('doctor_id', 'start_time')
    serializer_class = DoctorScheduleSerializer
