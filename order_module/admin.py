from django.contrib import admin

from order_module.models import Order, OrderItem, Address


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number',)
    ordering = ('order_number',)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'order_id', 'product_id', 'quantity')
    ordering = ('order', 'order_id')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Address)

