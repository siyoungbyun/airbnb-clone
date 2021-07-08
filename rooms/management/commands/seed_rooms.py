import random

from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from rooms import models as room_models
from users import models as user_models

from django_seed import Seed


class Command(BaseCommand):

    help = "This command seeds fake rooms."

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", help="The number of rooms to create", default=1, type=int
        )

    def handle(self, *args, **options):
        number = options.get("number", 0)
        try:
            seeder = Seed.seeder()
            # NOTE: bad practice to call all users
            all_users = user_models.User.objects.all()
            room_types = room_models.RoomType.objects.all()
            amenities = room_models.Amenity.objects.all()
            facilities = room_models.Facility.objects.all()
            rules = room_models.HouseRule.objects.all()
            seeder.add_entity(
                room_models.Room,
                number,
                {
                    "name": lambda x: seeder.faker.address(),
                    "host": lambda x: random.choice(all_users),
                    "room_type": lambda x: random.choice(room_types),
                    "price": lambda x: random.randint(1, 300),
                    "beds": lambda x: random.randint(1, 5),
                    "bedrooms": lambda x: random.randint(1, 5),
                    "baths": lambda x: random.randint(1, 5),
                    "guests": lambda x: random.randint(1, 5),
                },
            )
            created_photos = seeder.execute()
            created_clean = flatten(list(created_photos.values()))
            for pk in created_clean:
                room = room_models.Room.objects.get(pk=pk)
                for _ in range(3, random.randint(10, 30)):
                    room_models.Photo.objects.create(
                        caption=seeder.faker.sentence(),
                        room=room,
                        file=f"room_photos/{random.randint(1, 31)}.webp",
                    )
                # if magic_number is even, add to the room
                for amenity in amenities:
                    magic_number = random.randint(0, 15)
                    if magic_number % 2 == 0:
                        room.amenities.add(amenity)
                for facility in facilities:
                    magic_number = random.randint(0, 15)
                    if magic_number % 2 == 0:
                        room.facilities.add(facility)
                for rule in rules:
                    magic_number = random.randint(0, 15)
                    if magic_number % 2 == 0:
                        room.house_rules.add(rule)
            self.stdout.write(self.style.SUCCESS(f"{number} rooms created!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to create rooms: {e}"))
