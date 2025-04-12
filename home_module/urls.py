from django.urls import path
from .views import HomeView,AboutView

urlpatterns = [
    path('', HomeView.as_view() , name='home_page'),
    path('about-us/', AboutView.as_view(), name='about_page'),
]