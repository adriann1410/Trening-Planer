from django.template.defaulttags import register
from django.conf import settings
import os

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def placeholder_image(value):
    return os.path.join(value, settings.PLACEHOLDER_IMAGE_PATH)
