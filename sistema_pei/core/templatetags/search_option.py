#imports
from django.template import Library

register = Library()

#tag
@register.inclusion_tag(
    'templatetags/_search_option.html',
    takes_context=True
)
def search_option(context,object_name,query,input_placeholder=''):
    current_query = context.request.GET.get(object_name)
    current_input_value = query.filter(id=current_query).first()
    
    return {
        'current_query': current_query,
        'current_input_value' : current_input_value,
        'object_name' : object_name,
        'input_placeholder' : input_placeholder,
        'query' : query
    }

@register.inclusion_tag('templatetags/scripts/_search_script.html')
def load_search_script():
    return 