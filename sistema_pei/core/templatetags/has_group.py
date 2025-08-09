from django import template  # type: ignore
from django.db.models.functions import Lower

register = template.Library()

def user_has_some_groups(user,groups_list_lower:list)->bool:
    """verify if user at some group of list"""
    return user.groups.annotate(
        name_lower = Lower('name')
    ).filter(
        name_lower__in=groups_list_lower
    ).exists()


@register.filter
def has_group(user, group_name):
    """Verify if the user belongs to the specified group"""
    return user.groups.filter(name=group_name).exists()

@register.filter
def has_some_group(user,groups):
    groups_list = groups.split(' ')
    groups_list_lower = [group.lower() for group in groups_list]
    
    return user_has_some_groups(user,groups_list_lower)