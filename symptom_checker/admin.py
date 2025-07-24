from django.contrib import admin
from .models import Medicine, Disease, UserSymptom, VitalSign

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'healing_rate_7_days', 'typical_dosage')
    search_fields = ('name',)

@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'recommendation')
    search_fields = ('name',)
    filter_horizontal = ('medicine',)  # nice interface for many-to-many field

@admin.register(UserSymptom)
class UserSymptomAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'disease', 'created_at')
    list_filter = ('disease', 'created_at')
    search_fields = ('patient_id', 'symptoms')

@admin.register(VitalSign)
class VitalSignAdmin(admin.ModelAdmin):
    list_display = ('patient', 'disease', 'temperature', 'heart_rate', 'created_at')
    list_filter = ('disease', 'created_at')
    search_fields = ('patient__name',)
