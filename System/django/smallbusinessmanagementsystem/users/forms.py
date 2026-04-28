from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from users.models import User


class CustomPasswordResetForm(PasswordResetForm):

    def get_users(self, email):
        users = User.objects.filter(partner__person__email=email, is_active=True)
        return list(users)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(partner__person__email=email, is_active=True).exists():
            raise ValidationError(_("This email is not registered."))
        return email
