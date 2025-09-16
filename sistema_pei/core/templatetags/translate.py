from django.template import library
from django.utils.translation import gettext_lazy as _

register = library.Library()

@register.filter(name='translate')
def translate(value):
    value_lower = str(value).lower()
    return str(_(value_lower))
