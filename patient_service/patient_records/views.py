from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
import requests
from django.conf import settings
from .models import PatientRecord
from .serializers import PatientRecordSerializer

# Create your views here.

class PatientRecordViewSet(viewsets.ModelViewSet):
    queryset = PatientRecord.objects.all().order_by('-created_at')
    serializer_class = PatientRecordSerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

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

    def perform_create(self, serializer):
        auth_header = self.request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Thiếu hoặc sai định dạng token.')
        token = auth_header.split(' ')[1]
        user_info = self.get_user_info_from_token(token)
        user_id = user_info.get('id') or user_info.get('user_id')
        if not user_id:
            raise AuthenticationFailed('Không lấy được user_id từ user_service.')
        serializer.save(user_id=user_id)

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        auth_header = self.request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return Response({'detail': 'Thiếu hoặc sai định dạng token.'}, status=401)
        token = auth_header.split(' ')[1]
        user_info = self.get_user_info_from_token(token)
        user_id = user_info.get('id') or user_info.get('user_id')
        if not user_id:
            return Response({'detail': 'User not found in user_service.'}, status=404)
        record = PatientRecord.objects.filter(user_id=user_id).first()
        if not record:
            return Response({'detail': 'Not found.'}, status=404)
        serializer = self.get_serializer(record)
        return Response(serializer.data)
