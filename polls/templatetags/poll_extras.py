from django import template
import jdatetime
from datetime import datetime, date

register = template.Library()

@register.filter
def cut(value, arg):
    return value.replace(arg, "")


@register.filter
def to_jalali(value, fmt="%Y/%m/%d"):
    if not value:
        return "تاریخ نامعتبر"

    if isinstance(value, str):

        date_formats = ["%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y"]
        for date_format in date_formats:
            try:
                value = datetime.strptime(value, date_format)
                break
            except ValueError:
                continue

        else:
            return "فرمت تاریخ اشتباه است"

    if isinstance(value, (datetime, date)):
        try:
            # تاریخ شمسی به میلادی تبدیل
            jalali_date = jdatetime.datetime.fromgregorian(datetime=value)
            return jalali_date.strftime(fmt)
        except Exception as e:
            return f"خطا: {e}"

    return "فرمت تاریخ اشتباه است"


@register.filter(name="three_digits_currency")
def three_digits_currency(value: int):
    try:
        value = float(value)  # اگر اعشاری باشه هم درست کار کنه
        return '{:,.0f}'.format(value) + ' تومان'
    except (ValueError, TypeError):
        return str(value)

@register.simple_tag
def multiplay(quantity, price, *args, **kwargs):
    return three_digits_currency(quantity * price)

