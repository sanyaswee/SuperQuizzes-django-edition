from django import forms
from django.utils.translation import gettext_lazy as _

class FilterForm(forms.Form):
    search = forms.CharField(
        label=_("Search by name"), max_length=100, required=False,
        widget=forms.TextInput(attrs={"placeholder": _("Input quiz name")})
    )
    for_age = forms.IntegerField(
        label=_("Fine for"), min_value=1, max_value=99, required=False,
        widget=forms.NumberInput(attrs={'class': 'number-input'})
    )

    def __init__(self, *args, tags=None, **kwargs):
        kwargs.setdefault('label_suffix', '')  # disables colon
        super().__init__(*args, **kwargs)
        if tags:
            for tag in tags:
                self.fields[tag.tag] = forms.BooleanField(
                    label=tag.localized_uk_ua, required=False
                )


class AdvancedSearchForm(forms.Form):
    search = forms.CharField(required=False, label='', widget=forms.TextInput(attrs={
        'placeholder': _('Input quiz name')
    }))
    min_questions = forms.IntegerField(
        required=False,
        min_value=0,
        label=_("From"),
        widget=forms.NumberInput(attrs={'class': 'number-input'})
    )
    max_questions = forms.IntegerField(
        required=False,
        min_value=1,
        label=_("to"),
        widget=forms.NumberInput(attrs={'class': 'number-input'})
    )
    for_age = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=99,
        label='',
        widget=forms.NumberInput(attrs={'class': 'number-input'})
    )

    def __init__(self, *args, tags=None, **kwargs):
        super().__init__(*args, **kwargs)
        if tags:
            for tag in tags:
                self.fields[tag.tag] = forms.BooleanField(
                    required=False,
                    label=tag.localized_uk_ua,
                )
