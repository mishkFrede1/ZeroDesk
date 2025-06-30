from random import randint
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from MainApp.models import *
from MainApp.paginations import ArticlesPagination
from MainApp.permissions import IsNeuralNetUser
from MainApp.serializers import ArticleSerializer, CategoriesSerializer, TagsSerializer


class IndexView(ListView):
    template_name = "MainApp/home.html"
    context_object_name = "articles"
    queryset = Articles.objects.all()
    bottom_categories = ["Politics", "Science", "Technologies", "Sport", "Culture and art", "World"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(kwargs)
        context["articles"] = Articles.objects.exclude(category__name="Video Games")
        context["main_articles"] = context["articles"][:2]
        context["left_articles"] = context["articles"][2:6]
        context["latest_articles"] = context["articles"][6:17]
        context["categories"] = Categories.objects.all()[:9]
        context["popular_tags"] = Tags.objects.annotate(article_count=Count('tag_elements')).order_by('-article_count')[:50]
        categories_with_articles = []
        exclude_articles = [ article.pk for article in context["main_articles"]|context["left_articles"] ]
        for category in Categories.objects.filter(name__in=self.bottom_categories):
            articles = category.category_elements.order_by('-created_at').exclude(pk__in=exclude_articles)[:3]  # 3 свежих статьи
            categories_with_articles.append({
                'category': category,
                'first_article': articles[0],
                'articles': articles[1:]
            })
        context["categories_with_articles"] = categories_with_articles
        return context

class ArticleDetailView(DetailView):
    template_name = "MainApp/article.html"
    context_object_name = "article"
    slug_url_kwarg = "slug"

    def get_object(self, **kwargs):
        return get_object_or_404(Articles.objects, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(kwargs)
        sidebar_articles = context["article"].category.category_elements.exclude(title=context["article"].title)
        if len(sidebar_articles) > 5:
            random_num = randint(0, len(sidebar_articles)-5)
            context["sidebar_articles"] = sidebar_articles[random_num:random_num+5]
        else: context["sidebar_articles"] = sidebar_articles

        context["related_articles"] = (
            Articles.objects
            .exclude(pk=context["article"].pk)
            .filter(tags__in=context["article"].tags.all())
            .annotate(same_tags=Count('tags', filter=Q(tags__in=context["article"].tags.all())))
            .order_by('-same_tags', '-created_at')[:3]
        )
        context["related_articles_count"] = len(context["related_articles"])
        return context

class TagListView(ListView):
    template_name = "MainApp/tag.html"
    context_object_name = "articles"
    slug_url_kwarg = "tag_slug"
    paginate_by = 10
    tag = None

    def set_tag(self):
        self.tag = get_object_or_404(Tags.objects, slug=self.kwargs['tag_slug'])
        return self.tag

    def get_queryset(self):
        tag = self.set_tag()
        return Articles.objects.filter(tags__in=[tag])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(kwargs)
        context["tag"] = self.tag
        return context

class LatestListView(ListView):
    template_name = "MainApp/latest.html"
    context_object_name = "articles"
    paginate_by = 10

    def get_queryset(self):
        return Articles.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(kwargs)
        return context

class CategoryListView(ListView):
    template_name = "MainApp/category.html"
    context_object_name = "articles"
    paginate_by = 16

    def get_queryset(self):
        category = get_object_or_404(Categories, slug=self.kwargs['category_slug'])
        return category.category_elements.select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(kwargs)
        context["category"] = get_object_or_404(Categories, slug=self.kwargs['category_slug'])
        return context

class CategoriesListView(ListView):
    template_name = "MainApp/categories.html"
    context_object_name = "categories"
    queryset = Categories.objects.all()


class ArticlesViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Articles.objects.all()
    pagination_class = ArticlesPagination
    permission_classes = [IsAuthenticated, IsNeuralNetUser]

class CategoriesViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriesSerializer
    queryset = Categories.objects.all()
    pagination_class = None
    permission_classes = [IsAuthenticated, IsNeuralNetUser]

class TagsViewSet(viewsets.ModelViewSet):
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()
    lookup_field = "slug"
    pagination_class = None
    permission_classes = [IsAuthenticated, IsNeuralNetUser]


