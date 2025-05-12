from django import forms
from django.utils.translation import gettext_lazy as _

class FilterForm(forms.Form):
    search = forms.CharField(
        label=_("Search by name"),
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('Input quiz name')})
    )

    for_age = forms.IntegerField(
        label=_("Fine for"),
        min_value=1,
        max_value=99,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'number-input'})
    )
