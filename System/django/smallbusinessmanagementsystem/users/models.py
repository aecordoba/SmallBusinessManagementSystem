from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from partners.models import Partner


class UserManager(BaseUserManager):
    def create_user(self, name, password=None, **extra_fields):
        if not name:
            raise ValueError("Name is required")
        user = self.model(name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=30, unique=True, null=False, blank=False, help_text='Username')
    partner = models.OneToOneField(Partner, on_delete=models.RESTRICT, null=True, blank=True, related_name='partner')
    date_joined = models. DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.id)])

    @property
    def email(self):
        return self.partner.person.email

    class Meta:
        managed = True
        db_table = 'users'
        ordering = ['name']
