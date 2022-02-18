from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django import views

from .forms import UserRegistrationForm


class Register(views.View):
    def post(self, request):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password1"])
            new_user.save()
            return redirect("/")

    def get(self, request):
        user_form = UserRegistrationForm()
        return render(request, "app_users/register.html", {"user_form": user_form})


class Login(LoginView):
    template_name = "app_users/login.html"
    success_url = "/"


class Logout(LogoutView):
    template_name = "app_users/logout.html"
    success_url = "/"
