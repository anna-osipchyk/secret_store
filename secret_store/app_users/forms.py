from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    password_real = forms.CharField(label="Password", widget=forms.PasswordInput)
    password_repeat = forms.CharField(
        label="Repeat password", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "email")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password_real"] != cd["password_repeat"]:
            raise forms.ValidationError("Passwords don't match.")
        return cd["password_repeat"]
