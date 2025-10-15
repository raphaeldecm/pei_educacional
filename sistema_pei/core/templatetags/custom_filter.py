from django import template  # type: ignore  # noqa: PGH003

register = template.Library()


@register.filter
def custom_filter(dictionary, key):
    """Retorna o valor do dicionário pela chave, ou a própria chave se não existir"""
    return dictionary.get(key, key)
