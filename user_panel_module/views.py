from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from account_module.models import User
from order_module.models import Order, OrderItem
from .forms import EditProfileModelForm, ChangePasswordForm
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class UserPanelDashboardPageView(TemplateView):
    template_name = 'user_panel_module/user_panel_dashboard_page.html'


@method_decorator(login_required, name='dispatch')
class EditUserProfilePageView(View):
    def get(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(instance=current_user)
        context = {
            'form': edit_form,
            'current_user': current_user,
        }
        return render(request, 'user_panel_module/edit_profile_page.html', context)

    def post(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(request.POST, request.FILES, instance=current_user)
        if edit_form.is_valid():
            edit_form.save(commit=True)
        context = {
            'form': edit_form,
            'current_user': current_user,
        }
        return render(request, 'user_panel_module/edit_profile_page.html', context)


@method_decorator(login_required, name='dispatch')
class ChangePasswordView(View):
    def get(self, request: HttpRequest):
        context = {
            'form': ChangePasswordForm
        }
        return render(request, 'user_panel_module/change_password_page.html', context)

    def post(self, request: HttpRequest):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user: User = User.objects.filter(id=request.user.id).first()
            if user.check_password(form.cleaned_data.get('current_password')):
                user.set_password(form.cleaned_data.get('password'))
                user.save()
                logout(request)
                return redirect(reverse('login_page'))
            else:
                form.add_error('password', 'رمز عبور وارد شده اشتباه می باشد')
        context = {
            'form': form
        }
        return render(request, 'user_panel_module/change_password_page.html', context)


@login_required
def user_panel_menu_component(request: HttpRequest):
    return render(request, 'user_panel_module/components/user_panel_menu_component.html')


@login_required
def user_basket(request: HttpRequest):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_amount = current_order.calculate_total_price()

    context = {
        'order': current_order,
        'sum': total_amount,
    }
    return render(request, 'user_panel_module/user_basket.html', context)


@login_required
def remove_order_detail(request):
    detail_id = request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({
            'status': 'detail_id_not_found',
        })
    deleted_quantity, deleted_dict = OrderItem.objects.filter(id=detail_id, order__is_paid=False,
                                                              order__user_id=request.user.id).delete()

    if deleted_quantity is None:
        return JsonResponse({
            'status': 'detail_not_found',
        })
    current_order, created = Order.objects.prefetch_related('orderitem_set').get_or_create(is_paid=False,
                                                                                           user_id=request.user.id)
    total_amount = current_order.calculate_total_price()

    context = {
        'order': current_order,
        'sum': total_amount,

    }

    return JsonResponse({
        'status': 'success',
        'body': render_to_string('user_panel_module/user_basket_content.html', context),
    })


@login_required
def change_order_detail_count(request: HttpRequest):
    detail_id = request.GET.get('detail_id')
    # بررسی می‌کنیم که آیا پارامتر quantity نیز ارسال شده یا خیر
    quantity_param = request.GET.get('quantity')
    state = request.GET.get('state')

    if detail_id is None:
        return JsonResponse({
            'status': 'detail_id_not_found',
        })

    order_detail = OrderItem.objects.filter(
        id=detail_id,
        order__is_paid=False,
        order__user_id=request.user.id
    ).first()

    if order_detail is None:
        return JsonResponse({
            'status': 'detail_not_found',
        })

    # اگر پارامتر quantity ارسال شده باشد، مقدار به‌روز می‌شود
    if quantity_param is not None:
        try:
            new_quantity = int(quantity_param)
            if new_quantity < 1:
                new_quantity = 1
        except ValueError:
            new_quantity = order_detail.quantity
        order_detail.quantity = new_quantity
        order_detail.save()
    # در غیر اینصورت از پارامتر state استفاده می‌کنیم
    elif state == 'minus':
        if order_detail.quantity == 1:
            order_detail.delete()
        else:
            order_detail.quantity -= 1
            order_detail.save()
    elif state == 'plus':
        order_detail.quantity += 1
        order_detail.save()
    else:
        return JsonResponse({
            'status': 'state_invalid'
        })

    # به‌روزرسانی اطلاعات سبد خرید
    current_order, created = Order.objects.prefetch_related('orderitem_set').get_or_create(
        is_paid=False,
        user_id=request.user.id
    )
    total_amount = current_order.calculate_total_price()

    context = {
        'order': current_order,
        'sum': total_amount,
    }

    return JsonResponse({
        'status': 'success',
        'body': render_to_string('user_panel_module/user_basket_content.html', context),
    })
