#imports
from django.template import Library

register = Library()

#tag
@register.inclusion_tag(
    'templatetags/_search_option.html',
    takes_context=True
)
def search_option(context,input_name,query,input_placeholder=''):
    current_query = context.request.GET.get(input_name)
    current_input_value = query.filter(id=current_query).first()
    
    return {
        'current_query': current_query,
        'current_input_value' : current_input_value,
        'input_name' : input_name,
        'input_placeholder' : input_placeholder,
        'query' : query
    }