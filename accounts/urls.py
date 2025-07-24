from django.urls import path
from . import views
from .views import learn_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('signup/', views.register, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout_view'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('hero/', views.hero, name='hero'),
    path('learn/', learn_view, name='learn'),
    path('add_profile/', views.profile_view, name='add_profile'),
    path('admin/view-user/<int:user_id>/', views.view_user, name='view_user'),

]
