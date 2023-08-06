# Django TS Bridge

Creates a set of management commands that makes it easy to create TypeScript files that easy the usage of Django models within TypeScript

## Settings

- DJANGO_TS_BRIDGE_EXCLUDED_APPS - Array of apps that shouldn't be included in generation. Default: ['rest_framework', 'wagtail.api.v2']
- DJANGO_TS_BRIDGE_CHOICE_DEFINITION_IMPORT_PATH - The path used to import the generated TypeScript file of the choices available for all Django models. Default: 'ts/django/django-model-choices'
- DJANGO_TS_BRIDGE_CHOICE_DEFINITION_OUTPUT_PATH - The output path for the generated Typescript file of the choices available for all Django models. Default: 'src/ts/django/django-model-choices.ts'
- DJANGO_TS_BRIDGE_MODEL_DEFINITION_OUTPUT_PATH - The output path for the generated Typescript declaration file for all Django models. Default: 'src/ts/@types/django-models.d.ts'
- DJANGO_TS_BRIDGE_CHOICE_VAR_NAME - The name of the variable that will hold all Django model choices. Default: 'Choices'

## Management Commands

- create_ts_choice_defs - Creates a TypeScript file that defines all model choice fields based on its [models.TextChoices/models.IntegerChoices](https://docs.djangoproject.com/en/dev/ref/models/fields/#enumeration-types) class
- create_ts_serializer_types - Creates a TypeScript declaration file that defines all the interfaces that will be used by Django Rest Framework Serializer classes
- create_ts_files - Convience function to run both create_ts_choice_defs and create_ts_serializer_types at the same time