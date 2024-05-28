import csv
from django.core.management.base import BaseCommand
from restaurants.models import Restaurant

class Command(BaseCommand):
    help = 'Load restaurant data from CSV'

    def handle(self, *args, **kwargs):
        file_path = '/Users/parktaeji/Desktop/restaurant/restaurant_info1.csv'
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Restaurant.objects.create(
                    name=row['식당이름'],
                    category=row['식당종류'],
                    location=row['식당주소'],
                    service=row.get('서비스',''),
                    menu1=row.get('메뉴1', ''),
                    menu2=row.get('메뉴2', ''),
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded data'))
