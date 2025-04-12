from django.db import models
from account_module.models import User
from product_module.models import Product
import uuid

class Order(models.Model):
    ORDER_STATUS = (
        ('pending', 'در انتظار پرداخت'),
        ('processing', 'در حال پردازش'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل داده شده'),
        ('canceled', 'لغو شده'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    is_paid = models.BooleanField(default=False, verbose_name='نهایی شده / نهایی نشده')
    payment_date = models.DateTimeField(null=True, blank=True , verbose_name='تاریخ پرداخت')
    order_number = models.CharField(max_length=100, unique=True,editable=False, default=uuid.uuid4, verbose_name='کد سفارش سفارش',)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending', verbose_name='وضعیت سفارش')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'صفارش'
        verbose_name_plural = 'سفارشات'

    def __str__(self):
        return str(self.user)

    def calculate_total_price(self):
        total_amount = 0
        if self.is_paid:
            for orderitem in self.orderitem_set.all():
                total_amount += orderitem.final_price * orderitem.quantity
        else:
            for orderitem in self.orderitem_set.all():
                total_amount += orderitem.product.price * orderitem.quantity
        return total_amount



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سبد خرید')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    final_price = models.IntegerField(blank=True, null=True, verbose_name='قیمت نهایی محصول')
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد محصول سفارشی')

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

    class Meta:
        verbose_name = 'جزییات سفارش'
        verbose_name_plural = 'جزییات سفارشات'


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_addresses', verbose_name='کاربر')
    full_name = models.CharField(max_length=100,  verbose_name='نام و نام خانوادگی')
    phone = models.CharField(max_length=15, verbose_name='شماره تماس')
    province = models.CharField(max_length=50, verbose_name='استان')
    city = models.CharField(max_length=50, verbose_name='شهر')
    street = models.CharField(max_length=100, verbose_name='خیابان')
    postal_code = models.CharField(max_length=20, verbose_name='کد پستی')
    is_default = models.BooleanField(default=False, verbose_name='پیش فرض')

    def __str__(self):
        return f"{self.province}, {self.city}, {self.street}"

    class Meta:
        verbose_name = 'آدرس سفارش'
        verbose_name_plural = 'آدرس های سفارشات'


