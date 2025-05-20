from django.db import models

# Create your models here.
class Medication(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=20, blank=True)  # Đơn vị (viên, lọ, v.v.)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Diagnosis(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Prescription(models.Model):
    diagnosis = models.ForeignKey(Diagnosis, related_name='prescriptions', on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, related_name='prescriptions', on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.medication.name} ({self.dosage}) for {self.diagnosis.name}"

class LabTest(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    diagnosis = models.ForeignKey(Diagnosis, related_name='lab_tests', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
