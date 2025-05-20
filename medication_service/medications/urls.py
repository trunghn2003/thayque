from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicationViewSet, DiagnosisViewSet, PrescriptionViewSet, LabTestViewSet, SaveExamViewSet, ReminderViewSet

router = DefaultRouter()
router.register(r'medications', MedicationViewSet)
router.register(r'diagnoses', DiagnosisViewSet)
router.register(r'prescriptions', PrescriptionViewSet)
router.register(r'lab-tests', LabTestViewSet)
router.register(r'save-exam', SaveExamViewSet, basename='save-exam')
router.register(r'reminders', ReminderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
