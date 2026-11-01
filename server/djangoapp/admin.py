from django.contrib import admin
from .models import CarMake, CarModel

@admin.register(CarMake)
class MakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(CarModel)
class ModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'car_make', 'year', 'type', 'dealer_id']
    list_filter = ['car_make', 'year', 'type']
