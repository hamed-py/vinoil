from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, AuthLog

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ('phone',)
    list_display = ('phone', 'first_name', 'last_name', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name', 'avatar', 'about_user', 'address')}),
        ('مجوزها', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

@admin.register(AuthLog)
class AuthLogAdmin(admin.ModelAdmin):
    list_display = ('phone', 'event', 'success', 'timestamp')
    list_filter = ('event', 'success')