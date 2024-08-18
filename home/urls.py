from django.contrib import admin
from  django.urls import path
from .import views

from django.contrib.auth.models import User, auth



admin.site.site_header = "\xa9 Olaneye Ahmed"
admin.site.site_title = "Medinos Expense Tracker"
admin.site.index_title = f"Medinos Expense Tracker Admin Site"

urlpatterns = [
    path('', views.home, name = "home"),
    
]
