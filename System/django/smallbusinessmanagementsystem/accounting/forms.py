from django import forms
from django.utils.translation import gettext_lazy as _

class AddAccountingForm(forms.Form):
    date = forms.DateField(label=_('Date'), widget=forms.DateInput(attrs={'type': 'date'}), localize=True)
    concept = forms.CharField(label=_('Concept'))
    description = forms.CharField(label=_('Description'), widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}))
    debit = forms.DecimalField(label=_('Debit'), max_digits=15, decimal_places=2, localize=True, required=False)
    credit = forms.DecimalField(label=_('Credit'), max_digits=15, decimal_places=2, localize=True, required=False)

    def clean_date(self):
        data = self.cleaned_data['date']
        if data == "":
            raise ValidationError(_('Set a date.'))
        return data

    def clean_concept(self):
        data = self.cleaned_data['concept']
        if len(data) < 5 or len(data) > 30:
            raise ValidationError(_('The concept must be between 5 and 30 characters long.'))
        return data

    def clean_description(self):
        data = self.cleaned_data['description']
        if len(data) < 10 or len(data) > 100:
            raise ValidationError(_('The description must be between 10 and 100 characters long.'))
        return data
