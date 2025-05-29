from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class ProfileForm(forms.ModelForm):
    username = forms.CharField(
        label=_("Username"),
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': _("Enter your new username"),
            'class': 'form-control'
        }),
        help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.")
    )

    class Meta:
        model = User
        fields = ['username']

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

        # Set initial value to current username
        if user:
            self.fields['username'].initial = user.username

    def clean_username(self):
        username = self.cleaned_data.get('username')

        # Check if username is different from current
        if self.user and username == self.user.username:
            return username

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            raise ValidationError(_("A user with that username already exists."))

        return username

    def save(self, commit=True):
        if self.user:
            self.user.username = self.cleaned_data['username']
            if commit:
                self.user.save()
            return self.user
        return super().save(commit)


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Custom password change form with styling and translation support
    """
    old_password = forms.CharField(
        label=_("Current Password"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _("Enter your current password")
        }),
        strip=False,
    )

    new_password1 = forms.CharField(
        label=_("New Password"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _("Enter your new password")
        }),
        strip=False,
        help_text=_("Your password must contain at least 8 characters and can't be entirely numeric.")
    )

    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _("Confirm your new password")
        }),
        strip=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Update error messages for better UX
        self.error_messages['password_incorrect'] = _(
            "Your old password was entered incorrectly. Please enter it again."
        )
        self.error_messages['password_mismatch'] = _(
            "The two password fields didn't match."
        )
