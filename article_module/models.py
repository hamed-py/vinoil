from django.db import models

from account_module.models import User


class ArticleCategory(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='دسته بندی والد', null=True, blank=True)
    title = models.CharField(max_length=200, verbose_name='عنوان دسته بندی')
    url_title = models.CharField(max_length=200, unique=True, verbose_name='عنوان لینک')
    is_active = models.BooleanField(default=True, verbose_name='فعال بودن / فعال نبودن')

    class Meta:
        verbose_name = 'دسته بندی مقاله'
        verbose_name_plural = 'دسته بندی مقالات'

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان مقاله')
    slug = models.SlugField(max_length=400, db_index=True, allow_unicode=True, verbose_name='عنوان در url')
    image = models.ImageField(upload_to='images/articles', verbose_name='تصویر مقاله')
    short_description = models.TextField(verbose_name='توضیحات کوتاه')
    text = models.TextField(verbose_name='متن مقاله')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیر فعال')
    selected_categories = models.ManyToManyField(ArticleCategory, verbose_name='دسته بندی ها')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده')
    author_image = models.ImageField(upload_to='images/authors', null=True, blank=True)

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    def __str__(self):
        return self.title


class ArticleComment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='مقاله')
    parent = models.ForeignKey('ArticleComment', on_delete=models.CASCADE,verbose_name='والد', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    text = models.TextField(verbose_name='متن نظر')
    is_active = models.BooleanField(verbose_name='فعال / عیرفعال', default=True)


    class Meta:
        verbose_name = 'نظر مقاله'
        verbose_name_plural = 'نظرات مقاله'

    def __str__(self):
        return str(f"{self.user}")


