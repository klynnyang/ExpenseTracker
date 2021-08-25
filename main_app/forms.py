from django import forms

class EmailForm(forms.Form):
    recipient = forms.EmailField()
