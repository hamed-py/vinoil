from django.contrib.auth.models import User
from django.db import models


class Contact_Us(models.Model):
    name = models.CharField(max_length=100,null=True, blank=False, verbose_name='نام کاربر' )
    email = models.EmailField( max_length=254, verbose_name='ایمیل کاربر', blank=False, null=False)
    subject = models.CharField(max_length=100, blank=False, verbose_name='موضوع')
    message = models.TextField(verbose_name='متن پیام')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    response = models.TextField(verbose_name='متن پیام پاسخ', null=True, blank=True)
    is_read_by_admin = models.BooleanField(default=False, verbose_name='خوانده شده توسط ادمین')

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'لیست تماس با ما'

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)


