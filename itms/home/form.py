from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

from django.contrib.auth.models import User
from django import forms


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text="required.")
    last_name = forms.CharField(max_length=30, required=False, help_text="required.")
    email = forms.EmailField(max_length=254, help_text="required, please enter valid email address.")
    department = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "department",
        )


class ChangePasswordForm(PasswordChangeForm):
    pass
