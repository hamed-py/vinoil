from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from account_module.models import User
from django.utils.text import slugify
import uuid


class ProductCategory(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name='دسته بندی والد',related_name='subcategories')
    url_title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')
    image = models.ImageField(upload_to='product/product_category', verbose_name='عکس دسته بندی', null=True, blank=True)

    def __str__(self):
        return f'( {self.title} - {self.url_title} )'

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class ProductBrand(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام برند', db_index=True)
    url_title = models.CharField(max_length=300, verbose_name='نام در url', db_index=True)
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(default=False, verbose_name='حذف شده / حذف نشده')

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برندها'

    def __str__(self):
        return f"{self.title} ({self.is_active})"


class Product(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام محصول')
    category = models.ManyToManyField(
        ProductCategory,
        related_name='product_categories',
        verbose_name='دسته بندی ها')
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, verbose_name='برند', null=True, blank=True)
    price = models.IntegerField(verbose_name='قیمت')
    short_description = models.CharField(max_length=360, db_index=True, null=True, verbose_name='توضیحات کوتاه')
    description = models.TextField(verbose_name='توضیحات اصلی', db_index=True)
    image = models.ImageField(upload_to='product/product_images', verbose_name='تصویر محصول', null=True, blank=True)
    slug = models.SlugField(default="", null=False, db_index=True, blank=True, max_length=200, unique=True,
                            verbose_name='عنوان در url')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:

            base_slug = slugify(self.title, allow_unicode=True)
            unique_slug = f"{base_slug}-{str(uuid.uuid4()).hex[:4]}"
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.price})"

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


class ProductTag(models.Model):
    caption = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_tags')

    class Meta:
        verbose_name = 'تگ محصول'
        verbose_name_plural = 'تگ های محصولات'

    def __str__(self):
        return self.caption


class ProductVisit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name= 'محصول')
    ip = models.GenericIPAddressField(verbose_name='آی پی کاربر')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='کاربر')

    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدیدهای محصول'

    def __str__(self):
        return f"{self.product.title} ({self.ip})"


class ProductGallery(models.Model):
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='انتخاب دسته بندی محصول', null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField(upload_to='images/product_gallery', verbose_name='تصویر')

    class Meta:
        verbose_name = 'تصویر گالری'
        verbose_name_plural = ' گالری تصاویر'

    def __str__(self):
        return f"{self.product.title}"


class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    parent = models.ForeignKey('ProductComment',related_name='replies' , on_delete=models.CASCADE, verbose_name='والد', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    text = models.TextField(verbose_name='متن نظر')
    is_active = models.BooleanField(verbose_name='فعال / عیرفعال', default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'نظر محصول'
        verbose_name_plural = 'نظرات محصول'

    def __str__(self):
        return str(f"{self.user}")

    def clean(self):
        # جلوگیری از نظرات تکراری
        if ProductComment.objects.filter(
                user=self.user,
                product=self.product,
                text=self.text
        ).exists():
            raise ValidationError('شما قبلاً این نظر را ارسال کرده‌اید!')
