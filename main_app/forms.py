from main_app.models import Month, Purchase, Category, Retailer
from django import forms
from django.forms import ModelForm

class EmailForm(forms.Form):
    recipient = forms.EmailField()

class MonthForm(ModelForm):
    class Meta:
        model = Month
        fields = ['month']