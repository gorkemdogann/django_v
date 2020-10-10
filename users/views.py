from django.shortcuts import render

from django.views.generic import CreateView
from .forms import RegisterForm
from django.contrib.auth.views import LoginView, LogoutView

class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = RegisterForm

    success_url = '/'
# burda success_url demek başaraılı olursa '/' bu url'e git yani ilk sayfaya


class UserLogin(LoginView):
    template_name = 'users/login.html'


class UserLogout(LogoutView):
    template_name = 'users/login.html'





