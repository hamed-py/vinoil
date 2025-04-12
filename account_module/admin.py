from django.contrib import admin
from . import models

class AccountAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'mobile')


admin.site.register(models.User, AccountAdmin)
