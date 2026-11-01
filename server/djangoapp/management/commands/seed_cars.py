from django.core.management.base import BaseCommand
from djangoapp.models import CarMake, CarModel
import json
from pathlib import Path

class Command(BaseCommand):
    help = 'Load the demonstration vehicle catalog without duplicating rows'
    def handle(self, *args, **kwargs):
        path = Path(__file__).resolve().parents[2] / 'car_records.json'
        if path.exists():
            for row in json.loads(path.read_text()):
                make, _ = CarMake.objects.get_or_create(name=row['make'])
                CarModel.objects.update_or_create(car_make=make, name=row['model'], defaults={'year': row['year'], 'dealer_id': row['dealer_id'], 'type': row['bodyType'].upper()})
            self.stdout.write(self.style.SUCCESS('Loaded complete IBM car catalog'))
            return
        for brand, names in {'Toyota': ['Camry', 'RAV4'], 'Honda': ['Civic', 'CR-V'], 'Ford': ['Explorer', 'Escape'], 'BMW': ['330i', 'X3']}.items():
            make, _ = CarMake.objects.get_or_create(name=brand, defaults={'description': brand + ' vehicles'})
            for name in names:
                CarModel.objects.get_or_create(car_make=make, name=name, defaults={'year': 2025})
        self.stdout.write(self.style.SUCCESS('Seeded 4 makes and 8 models'))
