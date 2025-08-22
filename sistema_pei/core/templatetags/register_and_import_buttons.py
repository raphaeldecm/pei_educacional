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
    
    
@register.inclusion_tag(
    'components/_import_button.html'
)    
def import_button(text,link):
    return {
        'button_text': text,
        'link': reverse(link),
    }
    

@register.inclusion_tag(
    'templatetags/register_import_buttons.html'
)    
def register_and_import_buttons(register_text,register_link,import_text,import_link):
    return {
        'register_text' : register_text,
        'register_link': register_link,
        'import_text' : import_text,
        'import_link': import_link,
    }
    

