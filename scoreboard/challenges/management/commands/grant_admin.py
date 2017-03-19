from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Grant admin privileges by user ID'

    def add_arguments(self, parser):
        parser.add_argument('user_id', nargs='+', type=int)

    def handle(self, *args, **options):
        User = get_user_model()
        for pk in options['user_id']:
            try:
                instance = User.objects.get(pk=pk)
            except User.DoesNotExist:
                message = self.style.ERROR('User with ID "%s" does not exist.')
                self.stdout.write(message % (pk,))
            else:
                if instance.is_superuser:
                    message = 'User with ID "%s" is already a superuser.'
                    self.stdout.write(self.style.NOTICE(message % (pk,)))
                else:
                    instance.is_superuser = True
                    instance.save()
                    message = 'Granted admin to user with ID "%s".'
                    self.stdout.write(self.style.SUCCESS(message % (pk,)))
