from django import template

register = template.Library()

@register.filter
def format_count(value):
    value = int(value)
    if value < 1000:
        return str(value)
    elif value < 1_000_000:
        return '{} тыс'.format(round(value / 1000))
    elif value < 1_000_000_000:
        return '{} млн'.format(round(value / 1_000_000))
    else:
        return '{} млрд'.format(round(value / 1_000_000_000))