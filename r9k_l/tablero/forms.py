from django import forms

class crear_post(forms.Form):
    texto = forms.CharField(label="Texto del post")

class responder_post(forms.Form):
    texto = forms.CharField(label="Respuesta del Post")