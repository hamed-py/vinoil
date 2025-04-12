from django import template

register = template.Library()

@register.filter
def to_persian(value):
    persian_numbers = {'0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴', '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'}
    return ''.join(persian_numbers.get(i, i) for i in str(value))
