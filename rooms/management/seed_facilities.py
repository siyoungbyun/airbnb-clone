from django.core.management.base import BaseCommand
from rooms.models import Facility


class Command(BaseCommand):

    help = "This command seeds a list of facilities."

    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]
        count = 0
        for facility in facilities:
            if not Facility.objects.filter(name=facility):
                Facility.objects.create(name=facility)
                count += 1
        self.stdout.write(self.style.SUCCESS(f"{count} facilities created!"))
