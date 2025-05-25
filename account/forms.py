from django import forms
from django.contrib.auth.models import User
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