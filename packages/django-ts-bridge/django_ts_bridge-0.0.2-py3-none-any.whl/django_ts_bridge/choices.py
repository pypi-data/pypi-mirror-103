from django.apps import apps
from django.conf import settings
from django.template import loader

from . import settings as default_settings
from .core import is_model_choice

def generate_choices():
    choices = {}
    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            choice_enums = [cls_attribute for cls_attribute in model.__dict__.values() if is_model_choice(cls_attribute)]
            if len(choice_enums):
                choice_definitions = {}
                for enum in choice_enums:
                    choice_definition = {}
                    for name in enum.names:
                        choice_definition[name] = enum[name]
                    choice_definitions[enum.__name__] = choice_definition
                choices[app_config.label] = {}
                choices[app_config.label][model._meta.object_name] = choice_definitions
    return choices

def generate_ts():
    choices = generate_choices()
    ts_var_name = getattr(settings, 'DJANGO_TS_BRDIGE_CHOICE_VAR_NAME', default_settings.DJANGO_TS_BRIDGE_CHOICE_VAR_NAME)
    ts_content = loader.render_to_string(
        'django_ts_bridge/choices_ts.tpl',
        {
            'choices': choices,
            'ts_var_name': ts_var_name,
        },
    )
    return ts_content
