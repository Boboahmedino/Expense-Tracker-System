from expenses import views
from  django.urls import path
from . import views 
from .views import  activate_account


# from.views import LogoutView
urlpatterns = [
    path('register', views.register, name = 'register'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),
    path('login', views.login, name = 'login'),
    # path('verify-2fa', views.verify_2fa, name='verify_2fa'),
    path('logout', views.logout, name = 'logout'),    
    
    # path('logout', LogoutView.as_view(), name = 'logout'),
    
    

    
]
 