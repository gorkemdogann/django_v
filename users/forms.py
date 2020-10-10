from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# class Amac(models.Model):
#     title = models.CharField(max_length=250)


class RegisterForm(UserCreationForm):
    username = forms.CharField()
    email = forms.EmailField(max_length=100)
    password1 = forms.CharField()
    password2 = forms.CharField()


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','email','password1','password2')






