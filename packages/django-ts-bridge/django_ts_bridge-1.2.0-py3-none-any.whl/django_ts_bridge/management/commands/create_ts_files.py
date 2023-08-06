from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Creates all TS files used to define the structure of Django models'

    def handle(self, *args, **options):
        call_command('create_ts_choice_defs', *args, **options)
        call_command('create_ts_serializer_types', *args, **options)