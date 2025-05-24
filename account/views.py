from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _


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
