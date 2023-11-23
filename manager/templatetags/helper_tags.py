from django import template
import re

register = template.Library()

@register.filter
def to_str(value):
    print(value)
    try:
        match = re.search(r'<option.*?>(.*?)</option>', str(value))
        if match:
            test_str = match.group(1).replace(" ", "_")
            return test_str
    except (AttributeError, IndexError, TypeError):
        pass
    return ''