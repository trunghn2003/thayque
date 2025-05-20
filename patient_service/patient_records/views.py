from django.shortcuts import render
from rest_framework import viewsets
from .models import PatientRecord
from .serializers import PatientRecordSerializer

# Create your views here.

class PatientRecordViewSet(viewsets.ModelViewSet):
    queryset = PatientRecord.objects.all().order_by('-created_at')
    serializer_class = PatientRecordSerializer
