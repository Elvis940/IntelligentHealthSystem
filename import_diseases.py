import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_ai_viz.settings')
django.setup()

from symptom_checker.models import Disease, Medicine

def load_diseases():
    with open('diseases.json', 'r') as f:
        data = json.load(f)

    for disease_data in data['diseases']:
        disease, created = Disease.objects.update_or_create(
            name=disease_data['name'],
            defaults={
                'symptoms': disease_data.get('symptoms', ''),
                'test_results': disease_data.get('test_results', ''),
                'recommendation': disease_data.get('recommendation', '')
            }
        )

        for med_data in disease_data.get('medicine', []):
            medicine, _ = Medicine.objects.update_or_create(
                name=med_data['name'],
                defaults={
                    'healing_rate_7_days': med_data.get('healing_rate', 70),
                    'description': f"Used for {disease_data['name']}"
                }
            )
            disease.medicine.add(medicine)

        # Signal will update medicine_text automatically, no need to do it here.

        print(f"✅ Processed {disease.name} with {disease.medicine.count()} medicines")

    print("\n✅ All diseases and medicines imported/updated successfully.")

if __name__ == '__main__':
    load_diseases()
