from tabnanny import verbose
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Profile (models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = 'Profiles'
        
class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(default = now)
    description = models.TextField()
    owner =models.ForeignKey(to = User, on_delete=models.CASCADE)
    category = models.CharField(max_length=300)
    
    def __str__ (self):
        return self.category
    
    class Meta:
        ordering = ['-date'] 
        
        
class Category(models.Model):
        name = models.CharField(max_length=300)

        class Meta:
            verbose_name_plural = 'Categories'

       
        def __str__ (self):
            return self.name
    