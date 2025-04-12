from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
import jdatetime
from datetime import datetime
from .models import Article, ArticleCategory, ArticleComment


class ArticleListView(ListView):
    model = Article
    paginate_by = 20
    template_name = 'article_module/articles_page.html'
    ordering = ['-created_at']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        recent_blogs = Article.objects.filter(is_active=True).order_by('-created_at')[:3]
        for article in context.get('object_list', []):
            if hasattr(article, 'created_at') and article.created_at:
                # بررسی نوع تاریخ
                if isinstance(article.created_at, jdatetime.datetime):
                    # اگر تاریخ از قبل جلالی است، مستقیماً فرمت بزن
                    article.jalali_created_at = article.created_at.strftime('%Y/%m/%d')
                elif isinstance(article.created_at, datetime):
                    # تبدیل تاریخ میلادی به جلالی
                    article.jalali_created_at = jdatetime.datetime.fromgregorian(
                        datetime=article.created_at
                    ).strftime('%Y/%m/%d')
                else:
                    article.jalali_created_at = "فرمت تاریخ اشتباه است"

        context['article_list'] = context.get('object_list', [])
        context['recent_blogs'] = recent_blogs
        return context

    def get_queryset(self):
        query = super(ArticleListView, self).get_queryset()
        query = query.filter(is_active=True)
        category_name = self.kwargs.get('category')
        if category_name is not None:
            query = query.filter(selected_categories__url_title__iexact=category_name)
        return query


def article_categories_component(request: HttpRequest):
    main_categories = ArticleCategory.objects.prefetch_related('articlecategory_set').filter(parent_id=None, is_active=True)
    context = {
        'main_categories': main_categories,
    }
    return render(request, 'article_module/components/article_categories_page.html', context)


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_module/article_detail_page.html'

    def get_queryset(self):
        query = super(ArticleDetailView, self).get_queryset()
        query = query.filter(is_active=True)
        return query

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data()
        article: Article = kwargs.get('object')
        context['comments'] = ArticleComment.objects.filter(article_id=article.id,
                                                            is_active=True).order_by('-created_at').prefetch_related(
            'articlecomment_set')

        context['comments_count'] = ArticleComment.objects.filter(article_id=article.id, is_active=True).count()
        context['recent_blogs'] = Article.objects.filter(is_active=True).order_by('-created_at').prefetch_related(
            'articlecomment_set'
        )
        return context


@login_required(login_url='login_page')
def add_article_comment(request: HttpRequest):
    if request.user.is_authenticated:
        article_id = request.POST.get('article_id')
        article_comment = request.POST.get('article_comment')
        parent_id = request.POST.get('parent_id')
        new_comment = ArticleComment(article_id=article_id, text=article_comment, user_id=request.user.id, parent_id=parent_id)
        new_comment.save()
        context = {
            'comments': ArticleComment.objects.filter(article_id=article_id, parent=None,
                                                            is_active=True).order_by('-created_at').prefetch_related(
            'articlecomment_set'),
            'comments_count': ArticleComment.objects.filter(article_id=article_id).count(),
        }
        return render(request,'article_module/includes/article_comments_partial.html', context)

    return HttpResponse('response')
