from django.contrib import admin
from .models import Expense, Category
# Register your models here.
# django from what i learned allows admin to store whatever action carried out in the models.py 
# and give from the administrative access to edit or correct



admin.site.register(Expense)
admin.site.register(Category)


# i created my super user and i created categories
# then migrate