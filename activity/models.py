from django.db import models
from accounts.models import User
# Create your models here.

class Activity(models.Model):
    CATEGORY_CHOICES = [
        ('transport', 'Transport'),
        ('diet', 'Diet'),
        ('energy', 'Energy'),
    ]

    TRANSPORT_CHOICES = [
        ('car', 'Car'),
        ('bike', 'Bike'),
        ('bus', 'Bus'),
    ]

    DIET_CHOICES = [
        ('veg', 'Vegetarian'),
        ('non_veg', 'Non-Vegetarian'),
        ('vegan', 'Vegan'),
    ]

    ENERGY_CHOICES = [
        ('appliances', 'Home Appliances'),
        ('lighting', 'Lighting'),
        ('heating', 'Heating'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    type = models.CharField(max_length=20, blank=True, null=True)
    description = models.CharField(max_length=255)
    carbon_emission_kg = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category} ({self.type}) - {self.carbon_emission_kg}kg"