from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import *
# Create your views here.
from django.urls import reverse

from .forms import UserRegistrationForm


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()
            return redirect('/')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'app_users/register.html', {'user_form': user_form})


class Login(LoginView):
    template_name = "app_users/login.html"
    success_url = "/"
