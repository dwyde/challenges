from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Creates a default user'

    def handle(self, *args, **options):
        try:
            User.objects.get(username=settings.DEFAULT_USERNAME)
        except User.DoesNotExist:
            User.objects.create_user(
                username=settings.DEFAULT_USERNAME,
                password=settings.DEFAULT_PASSWORD,
            )
            self.stdout.write(self.style.SUCCESS('Successfully created a default user'))
