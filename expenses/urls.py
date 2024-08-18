
from  django.urls import path
from .import views
# for password change
from django.contrib.auth import views as auth_views
from .views import PasswordsChangeView


urlpatterns = [
    path('profile', views.profile, name = 'profile'),
    path('change_password', PasswordsChangeView.as_view(template_name ='dashboard/password.html' ), name = 'change_password'),
    path('success', views.success, name = 'success' ), 
    path('expense_history', views.expense_history, name = 'expense_history'),
    path('add_expense', views.add_expense, name = "add_expense"),
    # i added a route / since i indicated an id in my views function,
    path('edit-expense/<int:id>', views.edit_expense, name = "edit_expense"),
    path('delete_expense/<int:id>', views.delete_expense, name = "delete_expense"),
    path('create_pdf_report', views.create_pdf_report, name = 'create_pdf_report'),
    path('My Expenses Record', views.csv_expense, name = "csv_expense"),
]
