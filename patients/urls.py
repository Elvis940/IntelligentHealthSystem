from django.urls import path
from . import views

urlpatterns = [
   path('', views.patients, name='patients'),
   path('patients/delete/<int:pk>/', views.delete_patient, name='delete_patient'),
   path('patients/edit/<int:pk>/', views.edit_patient, name='edit_patient'),
   path('patients/add/', views.add_patient, name='add_patient')
]

