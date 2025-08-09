from django import template  # noqa: INP001
from django.urls import reverse_lazy
from django.db.models.functions import Lower
from .has_group import user_has_some_groups

register = template.Library()

@register.inclusion_tag(
    "templatetags/breadcrumb_item.html",
    takes_context=True
)
def breadcrumb_item(context,text, icon, url=None, first=False,groups=None, **kwargs):  # noqa: FBT002
    link = None
    can_view_breadcumb = True
    
    if groups:
        request = context.get('request')
        user = request.user
        groups_list = groups.split(' ')
        groups_list_lower = [group.lower() for group in groups_list]
        
        can_view_breadcumb = user_has_some_groups(user,groups_list_lower)
        
    if url:
        k = {}
        if "pk" in kwargs:
            k["pk"] = kwargs.get("pk")
        link = reverse_lazy(url, kwargs=k)

    return {
        "text": text,
        "url": link,
        "icon": icon,
        "first": first,
        'can_view_breadcumb' : can_view_breadcumb
    }
