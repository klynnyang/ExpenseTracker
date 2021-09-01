from django.core.exceptions import NON_FIELD_ERRORS
from main_app.models import Month, Purchase, Category, Retailer, Budget
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from bootstrap_modal_forms.forms import BSModalModelForm

class EmailForm(forms.Form):
    recipient = forms.EmailField()

class MonthForm(ModelForm):
    class Meta:
        model = Month
        fields = ['month']

class BudgetForm(ModelForm):
    class Meta:
        model = Budget
        fields = ['name']

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

# import pprint
class PurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(PurchaseForm, self).__init__(*args, **kwargs)
        self.fields['budget'].queryset = Budget.objects.filter(user=self.request.user)
        self.fields['user'].queryset = User.objects.filter(username=self.request.user)
    
        
    # def clean(self):
    #     if not super(PurchaseForm, self).is_valid():
    #         pprint.pprint(vars(self))
    #         if not Retailer.objects.filter(name=self.data["retailer"]):
    #             retailer = Retailer(name=self.data["retailer"])
    #             retailer.save()

    #             # Purchase.objects.create(date = self.cleaned_data["date"], amount =self.cleaned_data["amount"], retailer = Retailer.objects.latest('id'), category = self.cleaned_data["category"], budget=self.cleaned_data["budget"])
    #             self.validate_unique()
    #     self.validate_unique()



        
    
