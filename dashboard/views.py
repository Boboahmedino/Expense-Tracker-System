from django.shortcuts import render
# from .models import Profile
# Create your views here.

# def profile(request):
    
#     profiles = Profile.objects.filter(user = request.user)
#     # data = Profile.objects.get(pk = 1)
#     current_user = request.user
#     Full_Name = current_user.username
#     Email = current_user.email
#     context = {
#         'profiles' : profiles,
#         'values' :profiles,
#         'Full_Name' : Full_Name,
#         'Email' : Email, 
      
       
#     }

#     return render(request, "dashboard/profile.html", context)





































# from django.contrib.auth.views import PasswordChangeView
# from .forms import PasswordChangingForm
# from django.urls import reverse_lazy

# class PasswordsChangeView(PasswordChangeView):
#     form_class = PasswordChangingForm
#     success_url = reverse_lazy('success')


# # Successful message after password change
# def success(request):
#     return render(request, 'dashboard/password_success.html')
