from django.db import models
from django.urls import reverse
from django.shortcuts import redirect
# Create your models here.

class Budget(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    
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
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    budget = models.ForeignKey(Budget, default=1, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, default=1, on_delete=models.CASCADE)
    retailer = models.ForeignKey(Retailer, default=1, on_delete=models.CASCADE)
    notes = models.TextField(max_length=100, blank=True, default='none')

    def get_absolute_url(self):
        return reverse('detail', kwargs={'budget_id': self.budget.id})

    def __str__(self):
        return f"{self.id}: {self.amount} from {self.retailer} on {self.date}"

