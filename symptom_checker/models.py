from django.db import models
from patients.models import Patient

class Medicine(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    healing_rate_7_days = models.FloatField(
        default=70,
        help_text="Effectiveness rating (10-100) for 7-day recovery"
    )
    typical_dosage = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.healing_rate_7_days}%)"

class Disease(models.Model):
    name = models.CharField(max_length=255, unique=True)
    symptoms = models.TextField()
    test_results = models.TextField(blank=True, null=True)
    recommendation = models.TextField(blank=True, null=True)
    medicine = models.ManyToManyField(Medicine, related_name='diseases', blank=True)

    # Legacy comma-separated medicines
    medicine_text = models.TextField(
        blank=True, 
        null=True,
        help_text="Legacy field - comma-separated medicine names"
    )

    def __str__(self):
        return self.name

    @property
    def medicine_list(self):
        """Backward compatible property"""
        return self.medicine_text if self.medicine_text else ", ".join([m.name for m in self.medicine.all()])

class UserSymptom(models.Model):
    patient_id = models.CharField(max_length=255)
    symptoms = models.TextField()
    disease = models.ForeignKey(
        Disease, 
        blank=True, 
        null=True, 
        on_delete=models.SET_NULL,
        related_name='user_symptoms'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Symptoms for Patient {self.patient_id} - {self.disease.name if self.disease else 'Unknown Disease'}"

    @property
    def recommendations(self):
        return self.disease.recommendation if self.disease else None

    @property
    def medicine(self):
        if self.disease:
            if self.disease.medicine.exists():
                return ", ".join([m.name for m in self.disease.medicine.all()])
            return self.disease.medicine_text
        return None

class VitalSign(models.Model):
    patient = models.ForeignKey(
        Patient,
        related_name='vital_signs',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    disease = models.ForeignKey(
        Disease,
        related_name='vital_signs',
        on_delete=models.CASCADE
    )
    temperature = models.CharField(max_length=100, blank=True, null=True)
    heart_rate = models.CharField(max_length=100, blank=True, null=True)
    respiratory_rate = models.CharField(max_length=100, blank=True, null=True)
    blood_pressure = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vital signs for {self.patient} - {self.disease.name}"
