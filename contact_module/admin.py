from django.contrib import admin
from . import models

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject')
    search_fields = ('name', )
    list_filter = ('name','email',)


admin.site.register(models.Contact_Us, ContactAdmin)
