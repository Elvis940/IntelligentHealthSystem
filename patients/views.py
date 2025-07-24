from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import IntegrityError
from .forms import PatientRegistrationForm
from .models import Patient
from django.conf import settings
import random
import string
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Patient
from django.contrib import messages

def generate_password(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PatientRegistrationForm
from .models import Patient
from django.db import IntegrityError

def patients(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            patient_id = form.cleaned_data['patient_id']
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            status = form.cleaned_data['status']

            first_name, *last_parts = name.split(' ', 1)
            last_name = last_parts[0] if last_parts else ''

            # Check duplicates
            if Patient.objects.filter(email=email).exists():
                messages.error(request, f'Patient with email {email} already exists.')
                return redirect('patients')

            if Patient.objects.filter(patient_id=patient_id).exists():
                messages.error(request, f'A patient with ID {patient_id} already exists.')
                return redirect('patients')

            try:
                Patient.objects.create(
                    patient_id=patient_id,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    age=age,
                    gender=gender,
                    status=status,
                )
                messages.success(request, f'Patient {first_name} added successfully.')
                return redirect('patients')

            except IntegrityError as e:
                messages.error(request, f'Integrity error: {e}')
                return redirect('patients')
        else:
            # Form invalid
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect('patients')
    else:
        form = PatientRegistrationForm()

    patients = Patient.objects.all()
    return render(request, 'pages/patients.html', {'patients': patients})


def add_patient(request):
    form = PatientRegistrationForm()
    return render(request, 'pages/add_patient.html', {'form': form})



def is_doctor_or_admin(user):
    return user.is_authenticated and user.role in ['doctor', 'admin']

@login_required
@user_passes_test(is_doctor_or_admin)
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'pages/list.html', {'patients': patients})

@login_required
@user_passes_test(is_doctor_or_admin)
def delete_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient.delete()
    messages.success(request, "Patient deleted successfully.")
    return redirect('patients')

@login_required
@user_passes_test(is_doctor_or_admin)
def edit_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.age = request.POST['age']
        patient.gender = request.POST['gender']
        patient.status = request.POST['status']
        patient.save()
        messages.success(request, "Patient updated successfully.")
        return redirect('patients')
    return render(request, 'pages/edit.html', {'patient': patient})
