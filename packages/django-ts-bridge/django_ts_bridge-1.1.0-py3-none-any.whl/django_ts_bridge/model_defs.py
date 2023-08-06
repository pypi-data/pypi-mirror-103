from typing import List
from django.apps import AppConfig
from django.db import models
from .core import is_model_choice


def create_enum(app_config, model, field):
    enums: List[models.Choices] = [cls_attribute for cls_attribute in model.__dict__.values() if is_model_choice(cls_attribute)]
    enum_name = ''
    ts_type = ''
    # Try and find the enum definition of the choices field. TODO check to see if this will ever bite me in the ass.
    # cause 2 enums could in theory have the same definition, although that would be dumb and highly unlikely
    for enum in enums:
        if enum.choices == field.choices:
            enum_name = enum.__name__
            break
    # No enum was defined so set the type to be a list of all possible raw values
    if enum_name == '':
        for choice in field.choices:
            value = choice[0]
            if isinstance(value, int):
                ts_type += f'{choice[0]} | '
            else:
                ts_type += f'\'{choice[0]}\' | '
        ts_type = ts_type[:-2]
    else:
        ts_type = f'typeof Choices.{app_config.label}.{model._meta.object_name}.{enum_name}'
    return ts_type

def create_model_mappings(app_config: AppConfig):
    """Updates the custom mappings with related models and their type in ts"""
    mappings = {}
    for model in app_config.get_models():
        for field in model._meta.get_fields():
            field_name = field.name
            if field.related_model is not None:
                ts_type = f'{field.related_model.__name__}|number' # Always allow the related models to be defined by their pks
                mappings[field_name] = ts_type
            elif field.choices is not None:
                mappings[field_name] = create_enum(app_config, model, field)
    return mappings