from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from contact_module.models import Contact_Us, UserProfile
from site_module.models import SiteSettings
from .forms import ContactUsModelForm


class ContactUsView(CreateView):
    model = Contact_Us
    form_class = ContactUsModelForm
    template_name = 'contact_module/contact_us_page.html'
    success_url = reverse_lazy('home_page')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        setting: SiteSettings = SiteSettings.objects.filter(is_main_settings=True).first()
        context['site_setting'] = setting

        return context


def store_file(file):
    with open('media/image.jpg', 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)


class CreateProfileView(CreateView):
    template_name = 'contact_module/create_profile_page.html'
    model = UserProfile
    fields = '__all__'
    success_url = reverse_lazy('contact_us:profiles_page')

    def form_valid(self, form):
        print("فرم معتبر است")
        print("داده‌ها:", form.cleaned_data)
        if 'image' in self.request.FILES:
            print("فایل تصویر دریافت شد:", self.request.FILES['image'])
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProfilesView(ListView):
    model = UserProfile
    template_name = 'contact_module/profiles_list_page.html'
    context_object_name = 'profiles'
