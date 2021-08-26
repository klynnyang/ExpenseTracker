from main_app.models import Purchase, Category, Retailer
from django import forms
from django.forms import ModelForm

class EmailForm(forms.Form):
    recipient = forms.EmailField()

