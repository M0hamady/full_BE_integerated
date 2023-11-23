from django import template
import re

register = template.Library()
@register.filter
def to_str(value):
    match = re.search(r'<option.*?>(.*?)</option>',     str(value))
    test_str = match.group(1)
    return str(test_str)