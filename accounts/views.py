from cProfile import Profile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .models import Account
from .models import Profile
import cloudinary.uploader
from django.contrib.auth import logout
from django.contrib.auth import get_user_model, authenticate, login as auth_login

def hero(request):
    return render(request, 'pages/hero.html')

def learn_view(request):
    return render(request, 'accounts/learn.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                
                # Handle profile picture separately
                if 'profile_picture' in request.FILES:
                    try:
                        user.profile_picture = request.FILES['profile_picture']
                    except Exception as e:
                        messages.warning(request, 'Profile picture upload failed, but account was created')
                
                user.save()
                messages.success(request, 'Registration successful!')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Error during registration: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = get_user_model().objects.get(email=email)

            if not user.is_active:
                messages.error(request, 'Your account is not active. Please contact support.')
                return render(request, 'accounts/login.html')

            if user.check_password(password):
                auth_login(request, user)
                
                # Convert role to lowercase for consistent comparison
                role = user.role.lower() if user.role else None
                
                if role == "admin":
                    return redirect('admin_dashboard')
                elif role == "doctor":
                    return redirect('dashboard')  # Ensure this is your doctor dashboard URL
                else:
                    return redirect('nurse_dashboard')
            else:
                messages.error(request, 'Invalid password')

        except get_user_model().DoesNotExist:
            messages.error(request, 'Invalid credentials. Please check your email and password.')

        return render(request, 'accounts/login.html')

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def profile_view(request):
    return render(request, 'pages/profile.html', {'user': request.user})



def add_profile_view(request):
    return render(request, 'pages/add_profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    user = request.user

    # ✅ Safely get or create the profile
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.phone_number = request.POST.get('phone_number')

        profile.bio = request.POST.get('bio')
        profile.location = request.POST.get('location')
        profile.birth_date = request.POST.get('birth_date')

        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES['profile_picture']

        user.save()
        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile')  # Update this to your actual profile view name

    # Send both user and profile to the template
    return render(request, 'pages/edit_profile.html', {'user': user, 'profile': profile})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def view_user(request, user_id):
    user = get_object_or_404(Account, id=user_id)
    
    # Get or create profile if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=user)
    
    context = {
        'user': user,
        'profile': profile
    }
    return render(request, 'pages/view_user.html', context)
