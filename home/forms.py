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
        kwargs.setdefault('label_suffix', '')  # disables colon like FilterForm
        super().__init__(*args, **kwargs)
        if tags:
            for tag in tags:
                self.fields[tag.tag] = forms.BooleanField(
                    required=False,
                    label=tag.localized_uk_ua,
                )

    def clean(self):
        cleaned_data = super().clean()
        min_questions = cleaned_data.get('min_questions')
        max_questions = cleaned_data.get('max_questions')

        # Validate that min is not greater than max
        if min_questions is not None and max_questions is not None:
            if min_questions > max_questions:
                raise forms.ValidationError(
                    _("Minimum number of questions cannot be greater than maximum.")
                )

        return cleaned_data


class QuizForm(forms.Form):
    def __init__(self, questions, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for q in questions:
            choices = [(ans, ans) for ans in q.answers]
            self.fields[q.question] = forms.ChoiceField(
                label=q.question,
                choices=choices,
                widget=forms.RadioSelect,
                required=True,
            )

        # Extra hidden fields
        self.fields['quiz_id'] = forms.CharField(widget=forms.HiddenInput)
        self.fields['completed_as'] = forms.CharField(widget=forms.HiddenInput, initial='form')
        self.fields['start_time'] = forms.CharField(widget=forms.HiddenInput)
