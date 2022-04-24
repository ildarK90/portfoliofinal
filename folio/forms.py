from django.forms import ModelForm
from .models import Skills
from django import forms

class MailForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.CharField(max_length=255)
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
