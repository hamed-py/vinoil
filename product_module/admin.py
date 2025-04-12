from django.contrib import admin
from . import models




class ProductAdmin(admin.ModelAdmin):
    list_filter = ['category', 'is_active']
    list_display = ['title', 'price', 'is_active', 'is_delete']
    list_editable = ['price', 'is_active']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('slug',)


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']



class ProductVisitAdmin(admin.ModelAdmin):
    list_display = ['product', 'user']

class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'user']



admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductCategory, ProductCategoryAdmin)
admin.site.register(models.ProductTag)
admin.site.register(models.ProductBrand)
admin.site.register(models.ProductVisit, ProductVisitAdmin)
admin.site.register(models.ProductGallery)
admin.site.register(models.ProductComment, ProductCommentAdmin)

