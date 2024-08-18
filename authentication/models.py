# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
import string

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    two_factor_code = models.CharField(max_length=6, blank=True, null=True)
    two_factor_code_expiration = models.DateTimeField(blank=True, null=True)

    def generate_two_factor_code(self):
        self.two_factor_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.two_factor_code_expiration = timezone.now() + timezone.timedelta(minutes=10)
        self.save()
