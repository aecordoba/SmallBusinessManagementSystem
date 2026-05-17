from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import Event

class CreateEventForm(forms.Form):
    name = forms.CharField(label=_('Name'))
    automatic = forms.BooleanField(label=_('Automatic'), widget=forms.CheckboxInput(attrs={'id': 'automatic'}), required=False)
    date = forms.DateField(label=_('Date'), widget=forms.DateInput(attrs={'type': 'date'}), localize=True)
    time = forms.TimeField(label=_('Time'), widget=forms.TimeInput(attrs={'type': 'time', 'id': 'time'}), localize=True, required=False)
    attendants = forms.IntegerField(label=_('Attendants'), required=False, widget=forms.NumberInput(attrs={'id': 'attendants'}))
    description = forms.CharField(label=_('Description'), widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), required=False)
    charge = forms.DecimalField(label=_('Charge'), max_digits=10, decimal_places=2, localize=True, required=False)
    validity = forms.ChoiceField(label=_('Validity'), choices=Event.Validities.choices, required=False, widget=forms.Select(attrs={'id': 'validity'}))

    def clean_name(self):
        data = self.cleaned_data['name']
        if len(data) < 5 or len(data) > 30:
            raise ValidationError(_('The name must be between 5 and 30 characters long.'))
        return data

    def clean_date(self):
        data = self.cleaned_data['date']
        if data == "":
            raise ValidationError(_('Set a date.'))
        return data


class CreateNewsForm(forms.Form):
    event = forms.ModelChoiceField(queryset=Event.objects.filter(date__gt=timezone.now()), empty_label="", required=False)
    brief = forms.CharField(label=_('Header'))
    description = forms.CharField(label=_('Description'), widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}))

    def clean_brief(self):
        data = self.cleaned_data['brief']
        if len(data) < 5:
            raise ValidationError(_('You must enter a header.'))
        return data
