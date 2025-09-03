from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('شماره تلفن باید تنظیم شود.')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30, blank=True, verbose_name='نام')
    last_name = models.CharField(max_length=30, blank=True, verbose_name='نام‌خانوادگی')
    avatar = models.ImageField(upload_to='users/users_profile', null=True, verbose_name='تصویر کاربر')
    about_user = models.TextField(null=True, blank=True, verbose_name='درباره شخص')
    address = models.TextField(null=True, blank=True, verbose_name='آدرس')
    phone = models.CharField(max_length=15, unique=True, verbose_name='شماره تماس')
    phone_verified = models.BooleanField(default=False, verbose_name='تایید شماره / تایید نبودن شماره')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    is_staff = models.BooleanField(default=False, verbose_name='کارکنان؟ / غیرکارکنان')

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        if self.first_name is not '' and self.last_name is not '':
            return self.first_name + ' ' + self.last_name
        return self.phone

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    @property
    def avatar_url(self):
        try:
            return self.avatar.url if self.avatar else '/static/images/person_1.jpg'
        except ValueError:
            return '/static/images/person_1.jpg'

class AuthLog(models.Model):
    EVENT_CHOICES = [
        ('register', 'ثبت‌نام'),
        ('login', 'ورود'),
        ('reset', 'بازنشانی رمز'),
    ]
    phone = models.CharField(max_length=15, verbose_name='شماره تماس')
    event = models.CharField(max_length=20, choices=EVENT_CHOICES, verbose_name='وضعیت کاربر')
    success = models.BooleanField(verbose_name='موفق بودن / نبودن')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='زمان ورود')

    def __str__(self):
        return f"{self.phone} - {self.event} - {'موفق' if self.success else 'ناموفق'}"