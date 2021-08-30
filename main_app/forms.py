from main_app.models import Month, Purchase, Category, Retailer, Budget
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EmailForm(forms.Form):
    recipient = forms.EmailField()

class MonthForm(ModelForm):
    class Meta:
        model = Month
        fields = ['month']

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class PurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(PurchaseForm, self).__init__(*args, **kwargs)
        self.fields['budget'].queryset = Budget.objects.filter(user=self.request.user)
    
