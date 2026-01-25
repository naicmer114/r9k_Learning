from django import forms
from .models import posts, respuestas, usuarios


class registro_form(forms.Form):
    username = forms.CharField(label="Nombre de usuario", max_length=64, required=True)
    password_first = forms.CharField(max_length=64, required=True)
    password_first_confirm = forms.CharField(max_length=64, required=True)
    pass


class login_form(forms.Form):
    username = forms.CharField(label="Nombre de usuario", max_length=64, required=True)
    password_first = forms.CharField(max_length=64, required=True)
    pass


class crear_post(forms.ModelForm):
    class Meta:
        model = posts
        fields = {"texto", "img"}
        labels = {
            "texto": "",
            "img": "",
        }


class responder_post(forms.ModelForm):
    class Meta:
        model = respuestas
        fields = {"texto", "img"}
        labels = {
            "texto": "",
            "imagen": "",
        }
