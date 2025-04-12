from django.contrib import admin
from .models import ArticleCategory, Article, ArticleComment


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'url_title', 'parent', 'is_active')
    list_editable = ('is_active', 'parent', 'url_title')


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active', 'author')
    list_editable = ['is_active']
    list_display_links = ['title']

    def save_model(self, request, obj: Article, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)


class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'article')


admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleComment, ArticleCommentAdmin)
