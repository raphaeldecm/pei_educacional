from django import template  # type: ignore

register = template.Library()


@register.filter
def has_group(user, group_name):
    """Verify if the user belongs to the specified group"""
    return user.groups.filter(name=group_name).exists()
