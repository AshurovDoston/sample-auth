from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    age = forms.IntegerField(required=False, min_value=1, help_text="Optional. Enter your age.")

    class Meta:
        model = UserProfile
        # fields = UserCreationForm.Meta.fields + ("age", "phone")
        fields = ("email", "username", "age", "first_name", "last_name", "phone", "password1", "password2")

