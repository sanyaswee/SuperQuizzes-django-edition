from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.db.models import Avg
from django.utils import timezone

from .forms import ProfileForm

from home.models import Completion


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, _('Account created for %(username)s!') % {'username': username})
            # Log the user in after registration
            login(request, user)
            return redirect('index')  # Redirect to dashboard or home page
        else:
            messages.error(request, _('Please correct the errors below.'))
    else:
        form = UserCreationForm()

    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, _('Welcome back, %(username)s!') % {'username': username})
                # Redirect to next page if specified, otherwise to dashboard
                next_page = request.GET.get('next', 'index')
                return redirect(next_page)
            else:
                messages.error(request, _('Invalid username or password.'))
        else:
            messages.error(request, _('Invalid username or password.'))
    else:
        form = AuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, _('You have been logged out successfully.'))
    return redirect('login')


@login_required
def profile(request):
    """
    Profile page where users can view and edit their account information.
    """
    if request.method == 'POST':
        form = ProfileForm(request.POST, user=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, _('Your username has been updated successfully!'))
            return redirect('profile')
        else:
            messages.error(request, _('Please correct the errors below.'))
    else:
        form = ProfileForm(user=request.user)

    context = {
        'form': form,
        'user': request.user,
    }

    return render(request, 'auth/profile.html', context)


@login_required
def user_completions(request):
    """
    View to show all completions for the current user.
    """
    # Get all completions for the current user, ordered by most recent first
    completions = Completion.objects.filter(user=request.user).select_related('quiz').order_by('-end_time')

    # Calculate statistics
    total_completions = completions.count()

    # Calculate average score if there are completions
    if total_completions > 0:
        average_score = completions.aggregate(avg_score=Avg('score'))['avg_score']
        average_score = round(average_score, 1) if average_score else 0
    else:
        average_score = 0

    # Prepare completion data with additional calculations
    completion_data = []
    for completion in completions:
        # Calculate time taken in seconds
        time_taken = (completion.end_time - completion.start_time).total_seconds()

        completion_data.append({
            'quiz_name': completion.quiz.name,
            'quiz_id': completion.quiz.id,
            'score': completion.score,
            'time_taken': int(time_taken),
            'completion_date': completion.end_time,
            'completion_type': 'Quiz' if not completion.is_form else 'Form'
        })

    context = {
        'completions': completion_data,
        'total_completions': total_completions,
        'average_score': average_score,
        'user': request.user,
    }

    return render(request, 'auth/user_completions.html', context)