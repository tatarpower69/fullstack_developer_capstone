from django.db import models

class CarMake(models.Model):
    name = models.CharField(max_length=60, unique=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=60)
    dealer_id = models.PositiveIntegerField(default=1)
    year = models.PositiveIntegerField(default=2025)
    type = models.CharField(max_length=20, choices=[('SUV', 'SUV'), ('SEDAN', 'Sedan'), ('WAGON', 'Wagon')], default='SEDAN')
    def __str__(self):
        return f'{self.car_make} {self.name} ({self.year})'
