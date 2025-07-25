from django import template
from django.urls import reverse

#register
register = template.Library()

#funcs

@register.inclusion_tag(
    filename='templatetags/action_item.html',
)
def action_buttons(detail_view,edit_view,object):
    urls = {
        'detail_url' : reverse(detail_view,args=[object.pk]),
        'edit_url' : reverse(edit_view,args=[object.pk]),
        'object' : object
    }
    return urls