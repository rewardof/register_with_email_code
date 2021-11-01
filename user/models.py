from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models


class UserManager(BaseUserManager):
    def _create_user(self, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have email")
        if not phone_number:
            raise ValueError("User must have username")
        user = self.model(email=email, phone_number=phone_number, *extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, phone_number, password=None, **extra_fields):
        user = self._create_user(email, phone_number, password, **extra_fields)
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        user = self._create_user(email, phone_number, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('phone_number',)
    objects = UserManager()

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return self.email


class Code(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='register_code')
    code = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.user} - {self.code}'

