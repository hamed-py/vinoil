from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True, null=True, verbose_name='موبایل')
    email_active_code = models.CharField(max_length=100, verbose_name="کد فعال سازی ایمیل")
    avatar = models.ImageField(upload_to='users/users_profile', null=True)
    about_user = models.TextField(null=True, blank=True,verbose_name='درباره شخص')
    address = models.TextField(null=True, blank=True, verbose_name='آدرس')


    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        if self.first_name is not '' and self.last_name is not '':
            return self.first_name + ' ' + self.last_name
        return self.email
