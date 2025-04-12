from django.urls import path
from .views import ArticleListView, ArticleDetailView, add_article_comment

urlpatterns = [
    path('',ArticleListView.as_view(), name='articles_list'),
    path('cat/<str:category>',ArticleListView.as_view(), name='articles_by_category_list'),
    path('<int:pk>/',ArticleDetailView.as_view(), name='article_detail'),
    path('add-article-comment', add_article_comment, name='add_article_comment'),
]
