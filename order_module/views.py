from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from product_module.models import Product
from .models import Order, OrderItem


# Create your views here.
@login_required(login_url='login_page')
def add_product_to_order(request: HttpRequest):
    product_id = int(request.GET.get('product_id'))
    quantity = int(request.GET.get('count'))
    if quantity < 1:
        quantity = 1

    if request.user.is_authenticated:
        product = Product.objects.filter(id=product_id, is_active=True, is_delete=False).first()
        if product is not None:
            current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
            current_order_detail = current_order.orderitem_set.filter(product_id=product_id).first()
            if current_order_detail is not None:
                current_order_detail.quantity += quantity
                current_order_detail.save()
            else:
                new_detail = OrderItem(order_id=current_order.id, product_id=product_id, quantity=quantity)
                new_detail.save()

            return JsonResponse({
                'status': 'success',
                'text': 'محصول موردنظر با موفقیت به سبد خرید اضافه شد',
                'confirm_button_text': 'ممنون',
                'icon': 'success',

            })
        else:
            return JsonResponse({
                'status': 'not_found',
                'text': 'محصول موردنظر یافت نشد',
                'confirm_button_text': 'ممنون',
                'icon': 'warning',
            })
    else:
        return JsonResponse({
            'status': 'not_auth',
            'text': 'برای سفارش محصول ابتدا وارد سایت شوید',
            'confirm_button_text': 'ورود',
            'icon': 'warning',
        })
