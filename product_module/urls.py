from django.urls import path
from . import views
from .views import add_product_comment

urlpatterns = [
    path('', views.product_list_view.as_view(), name='product_list'),
    path('cat/<cat>', views.product_list_view.as_view(), name='product_categories_list'),
    path('brand/<brand>', views.product_list_view.as_view(), name='product_list_by_brand'),
    path('product-favorite/', views.add_product_favorate.as_view(), name='product_favorite'),
    path('products/<str:slug>/', views.product_detail_view.as_view(), name='product_detail'),
    path('add-product-comment', add_product_comment, name='add_product_comment'),


]
