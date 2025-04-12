from django.urls import path
from .views import add_product_to_order
urlpatterns = [
    path('add-to-order', add_product_to_order, name='add_product_to_order'),
]