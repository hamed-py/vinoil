from django.db.models import Sum
from django.db.models.aggregates import Count
from django.shortcuts import render
from django.views.generic.base import TemplateView
from product_module.models import Product, ProductCategory
from site_module.models import SiteSettings, FooterLinkBox, Slider, Takhfif


class HomeView(TemplateView):
    template_name = 'home_module/index_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        most_visit_products = Product.objects.filter(is_active=True, is_delete=False).annotate(
            visit_count=Count('productvisit')).order_by('-visit_count')[:8]
        context['sliders'] = Slider.objects.filter(is_active=True)
        context['categories'] = ProductCategory.objects.filter(is_active=True)
        context['takhfif'] = Takhfif.objects.filter(is_active=True)
        context['most_visit_products'] = most_visit_products
        context['latest_products'] = Product.objects.filter(is_active=True, is_delete=False).order_by('-created_at')[:8]

        most_bought_products = Product.objects.filter(orderitem__order__is_paid=True).annotate(order_count=Sum(
             'orderitem__quantity'
        )).order_by('-order_count')[:8]

        context['most_bought_products'] = most_bought_products

        return context


def site_header_component(request):
    setting: SiteSettings = SiteSettings.objects.filter(is_main_settings=True).first()
    context = {
        'site_setting': setting,
    }
    return render(request, 'shared/site_header_component.html', context)


def site_footer_component(request):
    setting: SiteSettings = SiteSettings.objects.filter(is_main_settings=True).first()
    footer_link_boxes = FooterLinkBox.objects.all()
    for item in footer_link_boxes:
        item.footerlink_set
    context = {
        'site_setting': setting,
        'footer_link_boxes': footer_link_boxes,
    }
    return render(request, 'shared/site_footer_component.html', context)


class AboutView(TemplateView):
    template_name = 'home_module/about_page.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        site_setting: SiteSettings = SiteSettings.objects.filter(is_main_settings=True).first()
        context['site_setting'] = site_setting
        return context


