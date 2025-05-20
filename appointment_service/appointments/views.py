from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from .models import Appointment, DoctorSchedule
from .serializers import AppointmentSerializer, DoctorScheduleSerializer
from rest_framework.permissions import IsAuthenticated
import requests
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

# Create your views here.

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all().order_by('-created_at')
    serializer_class = AppointmentSerializer

    def get_user_info_from_token(self, token):
        # Gọi user_service để xác thực token và lấy user info
        user_service_url = 'http://localhost:8004/api/users/me/'
        headers = {'Authorization': f'Bearer {token}'}
        # headers = {'Authorization':
        print("here-------------------")
        try:
            resp = requests.get(user_service_url, headers=headers, timeout=5)
            if resp.status_code == 200:
                return resp.json()
            else:
                print(f"Error: {resp.status_code} - {resp.text}")
                raise AuthenticationFailed('Token không hợp lệ hoặc user_service lỗi.')
        except requests.RequestException:
            raise AuthenticationFailed('Không thể kết nối user_service.')

    def perform_create(self, serializer):
        print("=== perform_create called ===")
        # Lấy token từ request
        auth_header = self.request.headers.get('Authorization', '')
        print(f"auth_header: {auth_header}")
        if not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Thiếu hoặc sai định dạng token.')
        token = auth_header.split(' ')[1]
        user_info = self.get_user_info_from_token(token)
        print(f"user_info: {user_info}")
        user_id = user_info.get('id') or user_info.get('user_id')
        if not user_id:
            raise AuthenticationFailed('Không lấy được user_id từ user_service.')
        serializer.save(patient_id=user_id)

class DoctorScheduleViewSet(viewsets.ModelViewSet):
    queryset = DoctorSchedule.objects.all().order_by('doctor_id', 'start_time')
    serializer_class = DoctorScheduleSerializer
    # permission_classes = [IsAuthenticated]
