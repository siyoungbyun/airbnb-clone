from django.core.management.base import BaseCommand
from users.models import User

from django_seed import Seed


class Command(BaseCommand):

    help = "This command seeds fake users."

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", help="The number of users to create", default=1, type=int
        )

    def handle(self, *args, **options):
        number = options.get("number", 0)
        try:
            seeder = Seed.seeder()
            seeder.add_entity(User, number, {"is_staff": False, "is_superuser": False})
            seeder.execute()
            self.stdout.write(self.style.SUCCESS(f"{number} users created!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to create users: {e}"))
