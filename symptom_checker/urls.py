# symptom_checker/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.analyze_symptoms, name='submit_symptoms'),
    path('diseases/', views.DiseaseListView.as_view(), name='disease_list'),
]
