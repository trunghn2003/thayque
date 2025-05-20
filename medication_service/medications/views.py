from django.shortcuts import render
from rest_framework import viewsets
from .models import Medication, Diagnosis, Prescription, LabTest
from .serializers import MedicationSerializer, DiagnosisSerializer, PrescriptionSerializer, LabTestSerializer

# Create your views here.

class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all().order_by('-created_at')
    serializer_class = MedicationSerializer

class DiagnosisViewSet(viewsets.ModelViewSet):
    queryset = Diagnosis.objects.all().order_by('-created_at')
    serializer_class = DiagnosisSerializer

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all().order_by('-created_at')
    serializer_class = PrescriptionSerializer

class LabTestViewSet(viewsets.ModelViewSet):
    queryset = LabTest.objects.all().order_by('-created_at')
    serializer_class = LabTestSerializer
