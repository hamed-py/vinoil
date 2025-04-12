from django.urls import path
from .views import UserPanelDashboardPageView, EditUserProfilePageView, ChangePasswordView, user_basket, \
    remove_order_detail, change_order_detail_count

urlpatterns = [
    path('', UserPanelDashboardPageView.as_view(), name='user_panel_dashboard'),
    path('change-pass/', ChangePasswordView.as_view(), name='change_password_page'),
    path('edit-profile/', EditUserProfilePageView.as_view(), name='edit_user_profile'),
    path('user-basket', user_basket, name='user_basket_page'),
    path('remove-order/', remove_order_detail, name='remove_order_ajax'),
    path('change-order-detail', change_order_detail_count, name='change_order_detail_ajax'),
    path('update-order-detail', change_order_detail_count, name='update_order_detail_ajax'),
]
