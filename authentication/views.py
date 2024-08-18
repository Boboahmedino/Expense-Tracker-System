from email import message
from genericpath import exists
from django import conf, views
from django.views import View
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import re
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str

# Create your views here.

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                print('Username has been used')
                messages.warning(request, 'Username has been used')
                return redirect('register')
            
            elif User.objects.filter(email=email).exists():
                print('Email has been used')
                messages.warning(request, 'Email has been used')
                return redirect('register')
            
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.set_password(password)
                user.is_active = False
                user.save()
                
                # Generate activation link
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                activation_link = request.build_absolute_uri(reverse('activate', kwargs={'uidb64': uid, 'token': token}))

                email_subject = 'Account Created Successfully'
                context = {
                    'username': username,
                    'activation_link': activation_link,
                    'expiry_days': 2,
                }
                template = render_to_string('authentication/email.html', context)
                email_body = template
                email_message = EmailMessage(
                    email_subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                )
                email_message.fail_silently = False
                email_message.send()
                
                print('User account created')
                messages.success(request, f'{user} your account has been created, Please check your mail to activate your account')
                return render(request, 'authentication/activate.html')
                # return redirect('login')
                
        elif len(password) < 6 or not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]+$', password):
            print('Password must be at least 6 characters long and alphanumeric, containing both letters and numbers')
            messages.error(request, 'Password must be at least 6 characters long and alphanumeric, containing both letters and numbers')
            return redirect('register')
        
        else:
            print("Password doesn't match")
            messages.error(request, "Password doesn't match")
            return redirect('register')
         
    else:
        return render(request, 'authentication/register.html')

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated. You can now sign in.')
            return redirect('login')
        else:
            messages.error(request, 'The activation link is invalid or has expired.')
            return redirect('register')
    except User.DoesNotExist:
        messages.error(request, 'The user does not exist.')
        return redirect('register')




def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            print(f'Welcome! {user} you are now logged in')
            messages.success(request, f'Welcome! {user} you are now logged in')
            return redirect('expense_history')
        else:
            print('Your username or password is incorrect, Please fill all fields correctly')
            messages.error(request, 'Your username or password is incorrect, fill all fields correctly')
            return redirect('login')
        
    else:
        return render(request, 'authentication/login.html')


# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
        
#         user = auth.authenticate(username=username, password=password)
#         # user = auth.authenticate(username = User.objects.get(email = username), password = password)

        
#         if user is not None:
#             auth.login(request, user)
#             print(f'Welcome! {user} you are now logged in')
#             messages.success(request, f'Welcome! {user} you are now logged in')
#             return redirect('expense_history')
#         else:
#             print('Your username or password is incorrect, Please fill all fields correctly')
#             messages.error(request, 'Your username or password is incorrect, fill all fields correctly')
#             return redirect('login')
        
#     else:
#         return render(request, 'authentication/login.html')

def logout(request):
    auth.logout(request)
    print("You have been logged out")
    messages.success(request, "You have been logged out")
    return redirect('login')

# class LogoutView(View):
#     def post(self, request):
#         auth.logout(request)
#         print("You have been logged out")
#         messages.success(request, "You have been logged out")
#         return redirect('login')
