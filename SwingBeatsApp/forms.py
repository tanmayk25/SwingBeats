from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, help_text='Enter First Name.')
    last_name = forms.CharField(max_length=30, help_text='Enter Last name')
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    device_id = forms.CharField(max_length=30, help_text='Enter Device ID.')
    gender = forms.CharField(max_length=1,help_text="Enter your gender")
    age = forms.IntegerField(help_text="Enter your weight in age")
    weight = forms.IntegerField(help_text="Enter your weight in Kilograms")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'device_id', 'gender', 'age', 'weight' )