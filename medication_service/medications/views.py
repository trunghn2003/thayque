from django.shortcuts import render
from rest_framework import viewsets
from .models import Medication, Diagnosis, Prescription, LabTest, Reminder
from .serializers import MedicationSerializer, DiagnosisSerializer, PrescriptionSerializer, LabTestSerializer, ReminderSerializer
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
import requests

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

    def get_user_info_from_token(self, token):
        user_service_url = 'http://localhost:8004/api/users/me/'
        headers = {'Authorization': f'Bearer {token}'}
        try:
            resp = requests.get(user_service_url, headers=headers, timeout=5)
            if resp.status_code == 200:
                return resp.json()
            else:
                raise AuthenticationFailed('Token không hợp lệ hoặc user_service lỗi.')
        except requests.RequestException:
            raise AuthenticationFailed('Không thể kết nối user_service.')

    def get_queryset(self):
        queryset = super().get_queryset()
        auth_header = self.request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            user_info = self.get_user_info_from_token(token)
            user_id = user_info.get('id') or user_info.get('user_id')
            if user_id:
                return queryset.filter(patient_id=user_id)
        return queryset.none()

class LabTestViewSet(viewsets.ModelViewSet):
    queryset = LabTest.objects.all().order_by('-created_at')
    serializer_class = LabTestSerializer

    def get_user_info_from_token(self, token):
        user_service_url = 'http://localhost:8004/api/users/me/'
        headers = {'Authorization': f'Bearer {token}'}
        try:
            resp = requests.get(user_service_url, headers=headers, timeout=5)
            if resp.status_code == 200:
                return resp.json()
            else:
                raise AuthenticationFailed('Token không hợp lệ hoặc user_service lỗi.')
        except requests.RequestException:
            raise AuthenticationFailed('Không thể kết nối user_service.')

    def get_queryset(self):
        queryset = super().get_queryset()
        auth_header = self.request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            user_info = self.get_user_info_from_token(token)
            user_id = user_info.get('id') or user_info.get('user_id')
            if user_id:
                return queryset.filter(patient_id=user_id)
        return queryset.none()

class PrescriptionInputSerializer(serializers.Serializer):
    medication = serializers.IntegerField()
    dosage = serializers.CharField()
    instructions = serializers.CharField(allow_blank=True, required=False)

class LabTestInputSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField(allow_blank=True, required=False)

class SaveExamSerializer(serializers.Serializer):
    appointment = serializers.IntegerField()
    patient_record = serializers.IntegerField()
    diagnosis = serializers.DictField()
    prescriptions = PrescriptionInputSerializer(many=True)
    labtests = LabTestInputSerializer(many=True)

class SaveExamViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = SaveExamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        # Tạo Diagnosis
        diag = Diagnosis.objects.create(
            name=data['diagnosis'].get('name', ''),
            description=data['diagnosis'].get('description', ''),
            appointment=data['appointment'],
            patient_record=data['patient_record']
        )
        # Tạo Prescription
        pres_objs = []
        for pres in data['prescriptions']:
            med = Medication.objects.get(id=pres['medication'])
            pres_obj = Prescription.objects.create(
                diagnosis=diag,
                medication=med,
                dosage=pres['dosage'],
                instructions=pres.get('instructions', ''),
                appointment=data['appointment'],
                patient_record=data['patient_record']
            )
            pres_objs.append(pres_obj)
        # Tạo LabTest
        lab_objs = []
        for lab in data['labtests']:
            lab_obj = LabTest.objects.create(
                name=lab['name'],
                description=lab.get('description', ''),
                diagnosis=diag,
                appointment=data['appointment'],
                patient_record=data['patient_record']
            )
            lab_objs.append(lab_obj)
        return Response({
            'diagnosis_id': diag.id,
            'prescription_ids': [p.id for p in pres_objs],
            'labtest_ids': [l.id for l in lab_objs]
        }, status=status.HTTP_201_CREATED)

class ReminderViewSet(viewsets.ModelViewSet):
    queryset = Reminder.objects.all().order_by('-remind_time')
    serializer_class = ReminderSerializer

    def get_user_info_from_token(self, token):
        user_service_url = 'http://localhost:8004/api/users/me/'
        headers = {'Authorization': f'Bearer {token}'}
        try:
            resp = requests.get(user_service_url, headers=headers, timeout=5)
            if resp.status_code == 200:
                return resp.json()
            else:
                raise AuthenticationFailed('Token không hợp lệ hoặc user_service lỗi.')
        except requests.RequestException:
            raise AuthenticationFailed('Không thể kết nối user_service.')

    def get_queryset(self):
        queryset = super().get_queryset()
        auth_header = self.request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            user_info = self.get_user_info_from_token(token)
            user_id = user_info.get('id') or user_info.get('user_id')
            if user_id:
                return queryset.filter(patient_id=user_id)
        return queryset.none()
