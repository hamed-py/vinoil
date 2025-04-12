from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.aggregates import Count
from django.http import HttpRequest, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from site_module.models import SiteBannerBox
from utils.http_service import get_client_ip
from utils.convertors import group_list
from .models import Product, ProductCategory, ProductBrand, ProductVisit, ProductGallery, ProductComment
from django.views.generic import ListView, DetailView


class product_list_view(ListView):
    model = Product
    template_name = 'product_module/product_list.html'
    ordering = ['price']
    paginate_by = 12
    context_object_name = 'product_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(product_list_view, self).get_context_data()
        query = Product.objects.all()
        product: Product = query.order_by('-price').first()
        bd_max_price = product.price if product is not None else 0
        context['bd_max_price'] = bd_max_price
        context['start_price'] = self.request.GET.get('start_price') or 0
        context['end_price'] = self.request.GET.get('end_price') or bd_max_price
        context['banners'] = SiteBannerBox.objects.filter(is_active=True,
                                                          position__iexact=SiteBannerBox.SiteBannerPosition.product_list)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            self.template_name = 'product_module/includes/product_item_partial.html'

        return context

    def get_queryset(self):
        query = super(product_list_view, self).get_queryset()
        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')
        request: HttpRequest = self.request

        search_query = self.request.GET.get('q')
        if search_query:
            query = query.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        category = self.request.GET.get('cat')
        if category:
            query = query.filter(category__slug=category)

        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')

        # فیلتر حداقل و حداکثر قیمت
        if start_price and start_price.isdigit():
            query = query.filter(price__gte=int(start_price))

        if end_price and end_price.isdigit():
            query = query.filter(price__lte=int(end_price))

        # فیلتر بر اساس برند
        if brand_name:
            query = query.filter(brand__url_title__iexact=brand_name)

        # فیلتر بر اساس دسته‌بندی
        if category_name:
            query = query.filter(category__url_title__iexact=category_name)

        return query


class product_detail_view(DetailView):
    template_name = 'product_module/product_detail.html'
    model = Product
    context_object_name = 'product'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_product = self.object
        request = self.request
        favorite_product_id = request.session.get('product_favorite')
        context['is_favorite'] = favorite_product_id == str(loaded_product.id)
        context['banners'] = SiteBannerBox.objects.filter(is_active=True,
                                                          position__iexact=SiteBannerBox.SiteBannerPosition.product_detail)
        context['product_galeries'] = group_list(list(ProductGallery.objects.filter(product_id=loaded_product.id).all()), 3)
        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id

        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip, product_id=loaded_product.id).exists()
        if not has_been_visited:
            new_visit = ProductVisit(ip=user_ip, user_id=user_id, product_id=loaded_product.id)
            new_visit.save()

        context['comments'] = ProductComment.objects.filter(product=loaded_product,parent__isnull=True ,is_active=True).order_by('-created_at').prefetch_related('replies')


        return context

@method_decorator(login_required, name='dispatch')
class add_product_favorate(View):
    def post(self, request):
        product_id = request.POST.get("product_id")  # مقدار ID را دریافت کنید
        if not product_id:
            return redirect("some-error-page")  # در صورت نبود مقدار مناسب، هدایت به صفحه خطا

        product = get_object_or_404(Product, id=product_id)  # تبدیل ID به شیء مدل
        request.session["product_favorite"] = product_id  # ذخیره در سشن
        return redirect(product.get_absolute_url())


def product_category_component(request: HttpRequest):
    product_categories = ProductCategory.objects.prefetch_related('subcategories', 'product_categories').filter(parent__isnull=True, is_delete=False, is_active=True)
    context = {
        'categories': product_categories,
    }
    return render(request, 'product_module/components/product_categories_component.html', context)


def product_brands_component(request: HttpRequest):
    product_brands = ProductBrand.objects.annotate(products_count=Count('product')).filter(is_delete=False,
                                                                                           is_active=True)

    context = {
        'brands': product_brands,
    }
    return render(request, 'product_module/components/product_brand_component.html', context)



@login_required
@require_POST  # فقط درخواست‌های POST را بپذیر
def add_product_comment(request: HttpRequest):
    product_id = request.POST.get('product_id')
    product_comment = request.POST.get('text')
    parent_id = request.POST.get('parent_id')

    # اعتبارسنجی داده‌های ورودی
    if not product_id or not product_comment:
        return HttpResponseBadRequest('لطفاً متن نظر را وارد کنید.')

    # ایجاد نظر جدید
    product = get_object_or_404(Product, id=product_id)
    parent = ProductComment.objects.filter(id=parent_id).first() if parent_id else None

    ProductComment.objects.create(
        product=product,
        user=request.user,
        text=product_comment,
        parent=parent,
        is_active=True
    )

    # بازگرداندن HTML به‌روزشده نظرات
    comments = ProductComment.objects.filter(product=product, parent__isnull=True)
    return render(request, 'product_module/includes/product_comment_partial.html', {'comments': comments})



