from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator


# Create your models here.

class UserRegistration(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    USER_ROLE = [
        ('P', 'Patient'),
        ('H', 'HealthCare Provider')
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, default='Jane')
    last_name = models.CharField(max_length=50, default='Doe')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: "
                                                                   "'+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    role = models.CharField(max_length=1, choices=USER_ROLE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} {self.last_name}"


class HealthInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='health_info')
    pregnancy_status = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    health_conditions = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} is due on {self.due_date}"


class HealthWorkerInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='healthworker_info')
    medical_license_number = models.CharField(max_length=50, unique=True)
    specialty = models.CharField(max_length=100)
    hospital_name = models.CharField(max_length=255)
    clinic_location = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_available = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} is a {self.specialty} in {self.clinic_location}"


class Consultation(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_consultations')
    health_worker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='worker_consultations')
    channel_name = models.CharField(max_length=255, unique=True)
    uid = models.IntegerField()
    token = models.CharField(max_length=500, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    app_id = models.CharField(max_length=255, default="")

    def __str__(self):
        return f"{self.patient.username} with {self.health_worker.username} on {self.created_at}"
