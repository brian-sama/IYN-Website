from django.core.management.base import BaseCommand
from core.models import Country

class Command(BaseCommand):
    def handle(self, *args, **options):
        countries = [
            {"name": "Zimbabwe", "code": "ZW"},
            {"name": "South Africa", "code": "ZA"},
            {"name": "Tanzania", "code": "TZ"},
            {"name": "Mozambique", "code": "MZ"},
            {"name": "Nicaragua", "code": "NI"},
            {"name": "El Salvador", "code": "SV"},
            {"name": "Switzerland", "code": "CH"}
        ]
        for data in countries:
            Country.objects.get_or_create(code=data["code"], defaults=data)
        print("Loaded 7 countries")
