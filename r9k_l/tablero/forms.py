from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class crear_post(forms.Form):
    texto = forms.CharField(label="Texto del post")

class responder_post(forms.Form):
    texto = forms.CharField(label="Respuesta del Post")