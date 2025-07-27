from django import template
from django.urls import reverse

#register
register = template.Library()

#funcs

@register.inclusion_tag(
    filename='templatetags/action_buttons.html',
)
def action_buttons(detail_view,edit_view,object,model_name,**kwargs):
    urls = {
        'detail_url' : reverse(detail_view,args=[object.pk]),
        'edit_url' : reverse(edit_view,args=[object.pk]),
        'object' : object,
        'model' : model_name,
        'kwargs': kwargs,
    }
    return urls


@register.inclusion_tag(
    'components/_action_item.html',
)
def action_item(message,default_icon,hover_icon,border_class,hover_class,is_delete_button=False,link='#',link_args=''): 
    return  {
        'message': message,
        'default_icon': default_icon,
        'hover_icon': hover_icon,
        'border_color': border_class,
        'hover_color': hover_class,
        'is_delete_button': is_delete_button,
        'link' : link,
        'link_args' : link_args
    }   