from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
class UserRegistration(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('signin') #url to redirect to once signin is done

class Login(LoginView):
    template_name = 'login.html' #template to render

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')  # Redirect to login after signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')  # Redirect to home after successful login
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'signin.html')  # Render the login page


def logout_view(request):
    logout(request)
    return redirect('signin')  # Redirect to the signin page after logout