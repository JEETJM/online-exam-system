from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserRegisterForm
from .models import Profile


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


# @login_required
# def dashboard(request):
#     profile, created = Profile.objects.get_or_create(user=request.user)
#     return render(request, 'accounts/dashboard.html', {'profile': profile})


def teacher_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and hasattr(
            u, 'profile') and u.profile.role == 'teacher'
    )(view_func)


def student_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and hasattr(
            u, 'profile') and u.profile.role == 'student'
    )(view_func)


@login_required
def dashboard(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    context = {
        'profile': profile,
        'total_exams': 0,
        'attempted_exams': 0,
        'passed_exams': 0,
        'failed_exams': 0,
    }

    return render(request, 'accounts/dashboard.html', context)
