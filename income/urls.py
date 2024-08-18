
from  django.urls import path
from .import views




urlpatterns = [
    path('income_history', views.income_history, name = 'income_history'),
    path('add-income', views.add_income, name = "add_income"),
    # i added a route / since i indicated an id in my views function,
    path('edit-income/<int:id>', views.edit_income, name = "edit_income"),
    path('delete_income/<int:id>', views.delete_income, name = "delete_income"),
    path('My Income Record', views.csv_income, name = "csv_income"),
]
