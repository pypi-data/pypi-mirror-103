import importlib
import inspect
import os
from types import ModuleType
from django.apps import AppConfig
from django.conf import settings
from django.core.management.base import BaseCommand
from rest_framework.serializers import Serializer

from ... import model_defs, settings as default_settings
from ...fields import ts_interface, get_ts

class Command(BaseCommand):
    help = 'Creates a TypeScript definition file for all models registered in DRF serializers under DJANGO_TS_BRIDGE_MODEL_DEFINITION_OUTPUT_PATH'

    def get_location(self):
        output_path = getattr(settings, 'DJANGO_TS_BRIDGE_MODEL_DEFINITION_OUTPUT_PATH', default_settings.DJANGO_TS_BRIDGE_MODEL_DEFINITION_OUTPUT_PATH)
        return os.path.join(settings.BASE_DIR, output_path)

    def handle(self, *args, **options):
        self.excluded_apps = getattr(settings, 'DJANGO_TS_BRIDGE_EXCLUDED_APPS', default_settings.DJANGO_TS_BRIDGE_EXCLUDED_APPS)
        from django.apps import apps
        for app_config in apps.get_app_configs():
            if app_config.name not in self.excluded_apps:
                self.handle_app_config(app_config)
        # Remove Serializer from type name since it's redundant in TS
        choices_import_path = getattr(settings, 'DJANGO_TS_BRIDGE_CHOICE_DEFINITION_IMPORT_PATH', default_settings.DJANGO_TS_BRIDGE_CHOICE_DEFINITION_IMPORT_PATH)
        ts = get_ts().replace('Serializer', '')
        ts = f'import {{ Choices }} from \'{choices_import_path}\';\n' + ts
        type_file_location = self.get_location()
        with open(type_file_location, 'w') as type_file:
            type_file.write(ts)
        self.stdout.write(self.style.SUCCESS(f'Type file sucessfully generated at {type_file_location}'))

    def handle_app_config(self, app_config: AppConfig):
        try: #Check to see the app has serializers
            serializers_module: ModuleType = importlib.import_module(app_config.name + '.serializers')
        except ImportError:
            return
        mappings = model_defs.create_model_mappings(app_config)
        serializers = inspect.getmembers(serializers_module, lambda member: self.is_serializer(member, serializers_module))
        for name, serializer in  serializers:
            # Get the class def and apply the ts_interface decorator to it
            base_class = getattr(serializers_module, name)
            ts_interface(mapping_overrides=mappings)(base_class)
    
    def is_serializer(self, member: object, module):
        """Checks to see if the given member is a serializer class and is a part of the given module"""
        return inspect.isclass(member) and issubclass(member, Serializer) and member.__module__ == module.__name__
