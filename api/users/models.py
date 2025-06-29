from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, contact_number, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required.")
        if not email:
            raise ValueError("Email is required.")
        if not contact_number:
            raise ValueError("Contact number is required.")

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            contact_number=contact_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, contact_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', CustomUser.Role.ADMIN)
        return self.create_user(username, email, contact_number, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):

    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        EMPLOYEE = 'employee', 'Employee'
        RESIDENT = 'resident', 'Resident'


    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
   
    # your custom fields:
    middlename = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField()
    contact_number = models.CharField(max_length=20)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.RESIDENT
    )
    profile = models.ImageField(upload_to='profiles/', blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "contact_number"]
    def __str__(self):
        return self.username
    
    objects = CustomUserManager()