from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)

class Predictions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="predictions")

    gender = models.IntegerField()
    age = models.IntegerField()
    hypertension = models.IntegerField()
    heart_disease = models.IntegerField()
    ever_married = models.IntegerField()
    work_type = models.CharField(max_length=50)
    residence_type = models.CharField(max_length=50)
    avg_glucose_level = models.FloatField()
    bmi = models.FloatField()
    smoking_status = models.CharField(max_length=50)

    stroke_prediction = models.BooleanField()
    message = models.CharField(max_length=255)
    risk_percentage = models.FloatField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Prediction for {self.user.username} at {self.created_at}"