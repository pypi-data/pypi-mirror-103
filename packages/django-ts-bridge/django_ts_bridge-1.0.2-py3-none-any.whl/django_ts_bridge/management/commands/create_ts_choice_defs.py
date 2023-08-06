import os
import sys

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.core.management.base import BaseCommand

from ... import settings as default_settings
from ...choices import generate_ts


class Command(BaseCommand):
    help = 'Creates a static choices.d.ts file for django-js-choices'

    def get_location(self):
        output_path = getattr(settings, 'DJANGO_TS_BRIDGE_CHOICE_DEFINITION_OUTPUT_PATH', default_settings.DJANGO_TS_BRIDGE_CHOICE_DEFINITION_OUTPUT_PATH)
        return os.path.join(settings.BASE_DIR, output_path)

    def handle(self, *args, **options):
        location = self.get_location()
        content = generate_ts()
        with open(location, 'w') as type_file:
            type_file.write(content)
        self.stdout.write(self.style.SUCCESS(f'Choices definition file sucessfully generated at {location}'))
