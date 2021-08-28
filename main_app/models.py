from django.db import models
from django.urls import reverse
from django.shortcuts import redirect
from django.core.validators import MinValueValidator
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.

MONTH_CHOICES = (
    (1, 'January'), 
    (2, 'February'), 
    (3, 'March'), 
    (4, 'April'),
    (5, 'May'), 
    (6, 'June'), 
    (7, 'July'), 
    (8, 'August'),
    (9, 'September'), 
    (10, 'October'), 
    (11, 'November'), 
    (12, 'December')
)

class Month(models.Model):
    month = models.CharField(max_length=2, choices=MONTH_CHOICES, default=datetime.now().month)

class Budget(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Retailer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Purchase(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField('Date of purchase')
    amount = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)])
    budget = models.ForeignKey(Budget, default=1, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, default=1, on_delete=models.CASCADE)
    retailer = models.ForeignKey(Retailer, default=1, on_delete=models.CASCADE)
    notes = models.TextField(max_length=100, blank=True, default='none')

    def get_absolute_url(self):
        return reverse('table_detail', kwargs={'budget_id': self.budget.id})

    def __str__(self):
        return f"{self.amount} from {self.retailer} on {self.date}"

