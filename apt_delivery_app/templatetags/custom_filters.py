from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(value, arg):
    try:
        return value.filter(meal_id=arg).first()
    except AttributeError:
        return None