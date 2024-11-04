import csv
import os

from django.core.management.base import BaseCommand

from app.settings import BASE_DIR
from losb.models import City


class Command(BaseCommand):
    def handle(self, *args, **options):
        #TODO: Check what happens when file doesn't exist
        with open(os.path.join(BASE_DIR, 'cities.csv'), encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                city, created = City.objects.get_or_create(
                    name=row[9]
                )
