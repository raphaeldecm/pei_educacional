from django import template  # noqa: INP001
from django.urls import reverse_lazy

register = template.Library()


@register.inclusion_tag("templatetags/breadcrumb_item.html")
def breadcrumb_item(text, icon, url=None, first=False, **kwargs):  # noqa: FBT002
    link = None

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
    }
