from django.contrib import admin
from .models import SiteSettings, FooterLink, FooterLinkBox, Slider, Takhfif, SiteBannerBox


class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')


class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'is_active')
    list_editable = ('url', 'is_active')

class TakhfifAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'is_active')

class SiteBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'is_active', 'position')



admin.site.register(Takhfif,TakhfifAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(SiteSettings)
admin.site.register(FooterLink, FooterLinkAdmin)
admin.site.register(FooterLinkBox)
admin.site.register(SiteBannerBox, SiteBannerAdmin)

