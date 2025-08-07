from django.contrib import admin
from .models import Contact_Us

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject')
    search_fields = ('name', )
    list_filter = ('name','email',)


admin.site.register(Contact_Us, ContactAdmin)
