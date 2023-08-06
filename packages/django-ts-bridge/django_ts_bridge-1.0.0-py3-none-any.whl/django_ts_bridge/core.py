import inspect
from django.db import models

def is_model_choice(cls_attribute):
    return inspect.isclass(cls_attribute) and issubclass(cls_attribute, models.Choices)