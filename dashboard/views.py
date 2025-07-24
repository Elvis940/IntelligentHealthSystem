from django.shortcuts import render
from symptom_checker.models import Medicine, UserSymptom, Disease
from django.shortcuts import get_object_or_404, render
from symptom_checker.models import UserSymptom
from django.contrib.auth import get_user_model

from django.shortcuts import render
from django.db.models import Count
import json

from patients.models import Patient
from symptom_checker.models import UserSymptom
# views.py
from django.shortcuts import render
from django.db.models import Count, Avg,FloatField
from django.utils.dateformat import DateFormat
import json


from patients.models import Patient
from django.db.models.functions import TruncMonth,Cast

def dashboard(request):
    patients = Patient.objects.all()

    # Disease frequency
    disease_counts = (
        UserSymptom.objects
        .values('disease__name')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    diseases = [item['disease__name'] or 'Unknown' for item in disease_counts]
    disease_values = [item['count'] for item in disease_counts]
    
    male_patients = Patient.objects.filter(gender='M').count()
    female_patients = Patient.objects.filter(gender='F').count()

    # Get the latest UserSymptom with a disease
    latest_symptom = (
        UserSymptom.objects
        .filter(disease__isnull=False)
        .order_by('-created_at')
        .first()
    )

    treatment_labels = []
    treatment_rates = []

    if latest_symptom and latest_symptom.disease:
        medicines = latest_symptom.disease.medicine.all()
        treatment_labels = [med.name for med in medicines]
        treatment_rates = [med.healing_rate_7_days for med in medicines]

    context = {
        'total_patients': patients.count(),
        'male_patients': male_patients,
        'female_patients': female_patients,
        'diseases': json.dumps(diseases),
        'disease_values': json.dumps(disease_values),
        'treatment_labels': json.dumps(treatment_labels),
        'treatment_recovery_rates': json.dumps(treatment_rates),
        'current_patient_id': latest_symptom.patient_id if latest_symptom else None,
        'current_disease': latest_symptom.disease.name if latest_symptom and latest_symptom.disease else None,
    }

    return render(request, 'dashboard/dashboard.html', context)



def diagnostics(request):
    return render(request, 'pages/diagnostics.html')

# from patients.models import Patient  # import Patient model



def users(request):
    return render(request, 'pages/users.html')


from django.core.paginator import Paginator
from django.shortcuts import render


def medical_records(request):
    record_list = UserSymptom.objects.all().order_by('-created_at')
    paginator = Paginator(record_list, 10)

    page_number = request.GET.get('page')
    records = paginator.get_page(page_number)

    return render(request, 'pages/medical_records.html', {'records': records})


def symptom_checker(request):
    return render(request, 'pages/symptom_checker.html')

from symptom_checker.models import UserSymptom

from django.shortcuts import render, redirect, get_object_or_404
from symptom_checker.models import UserSymptom
from django.db.models import Q

def test_results(request):
    query = request.GET.get('q', '')
    if query:
        test_results = UserSymptom.objects.filter(
            Q(disease__name__icontains=query) |
            Q(symptoms__icontains=query) |
            Q(user_id__icontains=query)
        ).order_by('-created_at')
    else:
        test_results = UserSymptom.objects.all().order_by('-created_at')

    return render(request, 'pages/test_results.html', {
        'test_results': test_results,
        'query': query
    })

def delete_test_result(request, pk):
    result = get_object_or_404(UserSymptom, pk=pk)
    result.delete()
    return redirect('test_results') 


def recommendations(request):
    return render(request, 'pages/recommendations.html')

def reports(request):
    return render(request, 'pages/reports.html')

def notifications(request):
    return render(request, 'pages/notifications.html')

def system_settings(request):
    return render(request, 'pages/system_settings.html')

def admin_users(request):
    return render(request, 'pages/admin_users.html')

def logout_view(request):
    return render(request, 'pages/logout.html')

def record_detail(request, pk):
    record = get_object_or_404(UserSymptom, pk=pk)
    return render(request, 'pages/record_detail.html', {'record': record})

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

def record_delete(request, id):
    if request.method == 'POST':
        record = get_object_or_404(UserSymptom, id=id)
        record.delete()
        messages.success(request, "Medical record deleted successfully.")
    return redirect('medical_records')


from django.shortcuts import render
from django.db.models import Count
from django.utils.timezone import now
from datetime import timedelta
from django.db.models.functions import TruncMonth
from patients.models import Patient
from django.db.models import Avg

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from accounts.models import Account
from patients.models import Patient
from symptom_checker.models import UserSymptom

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required
def admin_dashboard(request):
    # Cards Data
    total_patients = Patient.objects.count()
    active_users = Account.objects.filter(is_active=True).count()
    admins = Account.objects.filter(role='admin').count()
    doctors = Account.objects.filter(role='doctor').count()

    # Chart Data
    gender_counts = Patient.objects.values('gender').annotate(count=Count('id'))
    genders = [item['gender'] for item in gender_counts]
    gender_values = [item['count'] for item in gender_counts]

    status_counts = Patient.objects.values('status').annotate(count=Count('id'))
    statuses = [item['status'] for item in status_counts]
    status_values = [item['count'] for item in status_counts]

    disease_counts = UserSymptom.objects.values('disease__name').annotate(count=Count('id')).order_by('-count')
    diseases = [item['disease__name'] or 'Unknown' for item in disease_counts]
    disease_values = [item['count'] for item in disease_counts]

    context = {
        'total_patients': total_patients,
        'active_users': active_users,
        'admins': admins,
        'doctors': doctors,
        'genders': json.dumps(genders),
        'gender_values': json.dumps(gender_values),
        'statuses': json.dumps(statuses),
        'status_values': json.dumps(status_values),
        'diseases': json.dumps(diseases),
        'disease_values': json.dumps(disease_values),
    }

    return render(request, 'pages/admin_dashboard.html', context)


def manage_users(request):
    User = get_user_model()
    users = User.objects.all().order_by('id')
    
    context = {
        'users': users,
    }
    return render(request, 'pages/manage_users.html', context)



User = get_user_model()

from django.contrib import messages
# ... rest of imports

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.role = request.POST.get('role', user.role)
        user.is_active = bool(request.POST.get('is_active'))
        user.save()
        messages.success(request, 'User updated successfully.')
        return redirect('manage_users')

    return render(request, 'pages/edit_user.html', {'user': user})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('manage_users')
    return render(request, 'pages/delete_user_confirm.html', {'user': user})

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



from symptom_checker.models import Disease, UserSymptom, VitalSign
from patients.models import Patient
from django.db.models import Avg
import json

from django.db.models import Avg, FloatField
from django.db.models.functions import Cast
from django.db.models import Max
@login_required
def nurse_dashboard(request):
    # Summary counts
    total_patients = Patient.objects.count()
    male_patients = Patient.objects.filter(gender='M').count()
    female_patients = Patient.objects.filter(gender='F').count()

    # Diseases that have vitals
    diseases_with_vitals = Disease.objects.filter(vital_signs__isnull=False).distinct()

    # Get the newest Disease based on its latest VitalSign's created_at
    current_disease = (
        Disease.objects
        .filter(vital_signs__isnull=False)
        .annotate(latest_vital_time=Max('vital_signs__created_at'))

        .order_by('-latest_vital_time')
        .first()
    )

    latest_vital = None
    if current_disease:
        latest_vital_obj = (
            VitalSign.objects
            .filter(disease=current_disease)
            .order_by('-created_at')
            .first()
        )
        if latest_vital_obj:
            latest_vital = {
                'patient_name': str(latest_vital_obj.patient) if latest_vital_obj.patient else 'Unknown',
                'temperature': float(latest_vital_obj.temperature) if latest_vital_obj.temperature else None,
                'heart_rate': float(latest_vital_obj.heart_rate) if latest_vital_obj.heart_rate else None,
                'respiratory_rate': float(latest_vital_obj.respiratory_rate) if latest_vital_obj.respiratory_rate else None,
                'blood_pressure': float(latest_vital_obj.blood_pressure) if latest_vital_obj.blood_pressure else None,
                'notes': latest_vital_obj.notes or "None",
                'recorded_at': latest_vital_obj.created_at.strftime("%Y-%m-%d %H:%M"),
            }

    # Chart data
    disease_names = [d.name for d in diseases_with_vitals]
    disease_counts = [d.vital_signs.count() for d in diseases_with_vitals]

    summary_cards = [
        {'label': 'Total Patients', 'value': total_patients, 'color': 'primary', 'icon': 'fa-users'},
        {'label': 'Male Patients', 'value': male_patients, 'color': 'info', 'icon': 'fa-male'},
        {'label': 'Female Patients', 'value': female_patients, 'color': 'warning', 'icon': 'fa-female'},
        {'label': 'Diseases Tracked', 'value': diseases_with_vitals.count(), 'color': 'success', 'icon': 'fa-notes-medical'},
    ]

    context = {
        'summary_cards': summary_cards,
        'current_disease': current_disease,
        'latest_vital': latest_vital,
        'disease_names_json': json.dumps(disease_names),
        'disease_counts_json': json.dumps(disease_counts),
    }

    return render(request, 'pages/nurse_dashboard.html', context)




from symptom_checker.models import VitalSign

def vital_signs_list(request):
    query = request.GET.get('q')
    if query:
        vital_signs = VitalSign.objects.filter(disease__name__icontains=query)
    else:
        vital_signs = VitalSign.objects.all()
    
    return render(request, 'pages/vital_signs_list.html', {
        'vital_signs': vital_signs,
        'query': query or ''
    })




from .forms import VitalSignForm

def vital_sign_create(request):
    if request.method == 'POST':
        form = VitalSignForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Vital sign record created successfully.")
            return redirect('vital_signs_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = VitalSignForm()
    return render(request, 'pages/vital_sign_create.html', {'form': form})


def vital_sign_edit(request, pk):
    vital = get_object_or_404(VitalSign, pk=pk)
    if request.method == 'POST':
        form = VitalSignForm(request.POST, instance=vital)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vital sign updated successfully.')
            return redirect('vital_signs_list')
    else:
        form = VitalSignForm(instance=vital)
    return render(request, 'pages/vital_sign_form.html', {'form': form, 'vital': vital})

def vital_sign_delete(request, pk):
    vital = get_object_or_404(VitalSign, pk=pk)
    if request.method == 'POST':
        vital.delete()
        messages.success(request, 'Vital sign deleted successfully.')
        return redirect('vital_signs_list')
    return render(request, 'pages/vital_sign_confirm_delete.html', {'vital': vital})