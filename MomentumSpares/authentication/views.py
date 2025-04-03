from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
# Create your views here.
class UserRegistration(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('signin') #url to redirect to once signin is done
class Login(LoginView):
    template_name = 'login.html' #template to render