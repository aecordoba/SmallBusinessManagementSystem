from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Person, City, Partner
from datetime import date


class CreatePartnerForm(forms.Form):
    partner_number = forms.IntegerField(label=_('Partner number'))
    first_name = forms.CharField(label=_('First name'))
    last_name = forms.CharField(label=_('Last name'))
    doc_type = forms.ChoiceField(label=_('Document'), choices=Person.Documents.choices)
    doc_number = forms.IntegerField(label=_('Number'))
    social_security = forms.CharField(label=_('Social Security'))
    email = forms.EmailField(label=_('E-mail'))
    birthdate = forms.DateField(label=_('Birthdate'), widget=forms.DateInput(attrs={'type': 'date'}), localize=True)
    gender = forms.ChoiceField(label=_('Gender'), choices=Person.Genders.choices)
    address = forms.CharField(label=_('Address'))
    zip_code = forms.CharField(label=_('ZIP Code'))
    city = forms.ModelChoiceField(queryset=City.objects.all())
    phone = forms.CharField(label=_('Phone number'), required=False)
    cellphone = forms.CharField(label=_('Cell phone number'), required=False)
    incorporation = forms.DateField(label=_('Incorporation'), widget=forms.DateInput(attrs={'type': 'date'}), localize=True)
    position = forms.ChoiceField(label=_('Position'), choices=Partner.Positions.choices)
    status = forms.ChoiceField(label=_('Status'), choices=Partner.Status.choices)

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if len(data) < 2 or len(data) > 30:
            raise ValidationError(_('The first name must be between 2 and 30 characters long.'))
        return data

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        if len(data) < 2 or len(data) > 30:
            raise ValidationError(_('The last name must be between 2 and 30 characters long.'))
        return data

    def clean_doc_number(self):
        data = self.cleaned_data['doc_number']
        if data < 1000000:
            raise ValidationError(_('Incorrect ID number.'))
        return data

    def clean_social_security(self):
        data = self.cleaned_data['social_security']
        if len(data) > 15:
            raise ValidationError(_('The social security number must be up to 15 characters long.'))
        return data

    def clean_birthdate(self):
        data = self.cleaned_data['birthdate']
        if data > date.today():
            raise ValidationError(_('Incorrect birthdate.'))
        return data

    def clean_address(self):
        data = self.cleaned_data['address']
        if len(data) < 5 or len(data) > 30:
            raise ValidationError(_('The address must be between 5 and 30 characters long.'))
        return data

    def clean_phone(self):
        data = self.cleaned_data['phone']
        if len(data) > 0 and len(data) < 8 or len(data) > 10:
            raise ValidationError(_('The phone number must be between 8 and 10 digits long (without hyphens).'))
        return data

    def clean_cellphone(self):
        data = self.cleaned_data['cellphone']
        if len(data) > 0 and len(data) < 8 or len(data) > 10:
            raise ValidationError(_('The cell phone number must be between 8 and 10 digits long (without hyphens).'))
        return data

