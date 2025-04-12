from django.db import models


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, unique=True, db_index=True, verbose_name='نام سایت')
    site_url = models.URLField(verbose_name='دامنه سایت')
    addres = models.CharField(max_length=500, verbose_name=' آدرس ')
    phone = models.CharField(max_length=15,null=True,blank=True, verbose_name='تلفن ')
    email = models.EmailField(max_length=72,null=True,blank=True, verbose_name='ایمیل ')
    logo = models.ImageField(upload_to='site_logo', null=True, blank=True, verbose_name='لوگو سایت')
    about_us_text = models.TextField(verbose_name='متن درباره ما')
    copy_right = models.TextField(verbose_name='متن کپی رایت سایت')
    is_main_settings = models.BooleanField(default=False, verbose_name='تنظیمات اصلی سایت')

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات'

    def __str__(self):
        return self.site_name

class FooterLinkBox(models.Model):
    title = models.CharField(max_length=100, verbose_name= 'عنوان')

    class Meta:
        verbose_name = 'دسته بندی لینک های فوتر'
        verbose_name_plural = 'دسته بندی های لینک فوتر'

    def __str__(self):
        return self.title

class FooterLink(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    url = models.URLField(max_length=500, verbose_name='لینک')
    footer_link_box = models.ForeignKey(FooterLinkBox, on_delete=models.CASCADE, verbose_name='دسته بندی')

    class Meta:
        verbose_name = 'لینک فوتر'
        verbose_name_plural = 'لینک های فوتر'

    def __str__(self):
        return self.title


class Slider(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    url = models.URLField(max_length=500, verbose_name='لینک')
    url_title = models.CharField(max_length=200, verbose_name='عنوان لینک')
    description = models.TextField(verbose_name='توضیحات')
    image = models.ImageField(upload_to='sliders/', null=True, blank=True, verbose_name='تصویر اسلایدر')
    is_active = models.BooleanField(default=True, verbose_name='فعال بودن / فعال نبودن')
    start_date = models.DateField(null=True, verbose_name='تاریخ شروع')
    end_date = models.DateField(null=True, verbose_name='تاریخ پایان')

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدرها'

    def __str__(self):
        return self.title


class Takhfif(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان تخفیف')
    mizan_takhfif = models.CharField(max_length=40, verbose_name='میزان تخفیف', blank=True, null=True)
    url = models.URLField(max_length=500, verbose_name='لینک')
    url_title = models.CharField(max_length=200, verbose_name='عنوان لینک')
    description = models.TextField(verbose_name='توضیحات تخفیف')
    image = models.ImageField(upload_to='images/takhfif', null=True, blank=True, verbose_name='تصویر اسلایدر تخفیف')
    is_active = models.BooleanField(default=True, verbose_name='فعال بودن / فعال نبودن')
    start_date = models.DateField(null=True, verbose_name='تاریخ شروع')
    end_date = models.DateField(null=True, verbose_name='تاریخ پایان')


    class Meta:
        verbose_name = 'اسلایدر تخفیف'
        verbose_name_plural = 'اسلایدرهای تخفیف'

    def __str__(self):
        return self.title


class SiteBannerBox(models.Model):
    class SiteBannerPosition(models.TextChoices):
        product_list = 'product_list', 'صفحه لیست محصولات'
        product_detail = 'product_detail', 'صفحه جزییات محصول'
        about_us = 'about_us', 'صفحه درباره ما'

    title=models.CharField(max_length=240, verbose_name='عنوان بنر')
    url = models.URLField(max_length=500, null=True, blank=True, verbose_name='آدرس بنر')
    image = models.ImageField(upload_to= 'images/banners/',max_length=240, null=True, blank=True, verbose_name='تصویر بنر')
    is_active = models.BooleanField(verbose_name='فعال بودن /غیرفعال بودن')
    start_date = models.DateField(null=True, verbose_name='زمان شروع')
    end_date = models.DateField(null=True, verbose_name='زمان پایان')
    position = models.CharField(verbose_name='جایگاه نمایشی', choices=SiteBannerPosition.choices, max_length=200)

    class Meta:
        verbose_name = 'بنر تبلیغاتی'
        verbose_name_plural = 'بنرهای تبلیغاتی'

    def __str__(self):
        return self.title


