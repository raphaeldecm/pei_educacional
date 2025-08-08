from django.template import Library
from django.urls import reverse

register = Library()

@register.inclusion_tag(
    'components/_register_button.html',
)
def register_button(text,link):
    return {
        'button_text': text,
        'link': reverse(link),
    }