from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.

# class Profile (models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return self.user.username
    
#     class Meta:
#         verbose_name_plural = 'Profiles'