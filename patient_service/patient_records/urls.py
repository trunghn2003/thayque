from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientRecordViewSet

router = DefaultRouter()
router.register(r'patients', PatientRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
