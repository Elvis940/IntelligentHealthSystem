from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('diagnostics/', views.diagnostics, name='diagnostics'),
    # path('patients/', views.patients, name='patients'),
    path('users/', views.users, name='users'),
    path('medical_records/', views.medical_records, name='medical_records'),
    path('symptom_checker/', views.symptom_checker, name='symptom_checker'),
    path('test_results/', views.test_results, name='test_results'),
    path('test_results/delete/<int:pk>/', views.delete_test_result, name='delete_test_result'),
    path('recommendations/', views.recommendations, name='recommendations'),
    path('reports/', views.reports, name='reports'),
    path('notifications/', views.notifications, name='notifications'),
    path('system_settings/', views.system_settings, name='system_settings'),
    path('admin_users/', views.admin_users, name='admin_users'),
    # path('logout/', views.logout_view, name='logout_view'),
    path('medical_records/<int:pk>/', views.record_detail, name='record_detail'),
    path('dashboard/medical_records/delete/<int:id>/', views.record_delete, name='record_delete'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage_users/', views.manage_users, name='manage_users'),

    path('manage_users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('manage_users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('nurse/dashboard/', views.nurse_dashboard, name='nurse_dashboard'),
    path('nurse/vitals/', views.vital_signs_list, name='vital_signs_list'),
    path('nurse/vitals/create/', views.vital_sign_create, name='vital_sign_create'),
    path('vitals/<int:pk>/edit/', views.vital_sign_edit, name='vital_sign_edit'),
    path('vitals/<int:pk>/delete/', views.vital_sign_delete, name='vital_sign_delete'),

    

]

