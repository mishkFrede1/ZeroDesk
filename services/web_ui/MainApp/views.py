from random import randint
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.core import cache

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from MainApp.models import *
from MainApp.paginations import ArticlesPagination
from MainApp.permissions import IsNeuralNetUser
from MainApp.serializers import ArticleSerializer, CategoriesSerializer, TagsSerializer, RegionSerializer
from MainApp.utils import sort_values_list

class IndexView(ListView):
    template_name = "MainApp/home.html"
    context_object_name = "articles"
    queryset = Articles.objects.all()
    bottom_categories = ["Politics", "Science", "Technologies", "Sport", "Culture and art", "World"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(kwargs)
        context["articles"] = Articles.objects.exclude(category__name__icontains=["Video Games", "Culture and Art", "Entertainment"])
        context["main_articles"] = context["articles"][:2]
        context["left_articles"] = context["articles"][2:6]
        context["latest_articles"] = context["articles"][6:17]
        context["categories"] = Categories.objects.all().exclude(name__in=["Video Games", "Entertainment"])[:8]
        context["popular_tags"] = Tags.objects.annotate(article_count=Count('tag_elements')).order_by('-article_count')[:25]
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

    @staticmethod
    def get_article_ttl(article):
        age = (timezone.now() - article.created_at).total_seconds()
        if age < 3600:             # < 1 hour:
            return 60 * 5          # 5 minutes

        elif age < 86400:          # < 1 day
            return 60 * 30         # 30 minutes

        elif age < 7 * 86400:      # < 1 week:
            return 60 * 60 * 6     # 6 hours

        else:                      # older:
            return 60 * 60 * 24    # 24 hours

    def get_object(self, **kwargs):
        cached_article = cache.get(f"zerodesk_article:{self.kwargs['slug']}")
        if cached_article is None:
            article = get_object_or_404(Articles.objects, slug=self.kwargs['slug'])
            cache.set(f"zerodesk_article:{self.kwargs['slug']}", article, timeout=self.get_article_ttl(article))
            return article
        return cached_article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(kwargs)
        sidebar_articles = context["article"].category.category_elements.exclude(title=context["article"].title)
        if len(sidebar_articles) > 5:
            random_num = randint(0, len(sidebar_articles)-5)
            context["sidebar_articles"] = sidebar_articles[random_num:random_num+5]
        else: context["sidebar_articles"] = sidebar_articles

        related_articles_cached = cache.get(f"zerodesk_article_related:{self.kwargs['slug']}")
        if related_articles_cached is None:
            context["related_articles"] = (
                Articles.objects
                .exclude(pk=context["article"].pk)
                .filter(tags__in=context["article"].tags.all())
                .annotate(same_tags=Count('tags', filter=Q(tags__in=context["article"].tags.all())))
                .order_by('-same_tags', '-created_at')[:3]
            )
            cache.set(f"zerodesk_article_related:{self.kwargs['slug']}", context["related_articles"], timeout=60*60)
        else:
            context["related_articles"] = related_articles_cached

        context["related_articles_count"] = len(context["related_articles"])
        return context


def article_delete(request, slug):
    return HttpResponseRedirect(f"/admin/MainApp/articles/{Articles.objects.get(slug=slug).pk}/delete")


class TagListView(ListView):
    template_name = "MainApp/tag.html"
    context_object_name = "articles"
    slug_url_kwarg = "tag_slug"
    paginate_by = 10
    tag = None

    def set_tag(self):
        cached_tag = cache.get(f"zerodesk_tag:{self.kwargs['tag_slug']}")
        if cached_tag is None:
            self.tag = get_object_or_404(Tags.objects, slug=self.kwargs['tag_slug'])
            cache.set(f"zerodesk_tag:{self.kwargs['tag_slug']}", self.tag, timeout=60*60)
        else:
            self.tag = cached_tag

        return self.tag

    def get_queryset(self):
        tag = self.set_tag()
        cached_articles = cache.get(f"zerodesk_tag_articles:{self.kwargs['tag_slug']}")
        if cached_articles is None:
            articles = Articles.objects.filter(tags__in=[tag])
            cache.set(f"zerodesk_tag_articles:{self.kwargs['tag_slug']}", articles, timeout=60*10)
            return articles
        else:
            return cached_articles

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
        cached_category_elements = cache.get(f"zerodesk_category_elements:{self.kwargs['category_slug']}")
        if cached_category_elements is None:
            category_elements = category.category_elements.select_related('category')
            cache.set(f"zerodesk_category_elements:{self.kwargs['category_slug']}", category_elements, timeout=60*10)
            return category_elements
        else:
            return cached_category_elements

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(kwargs)
        context["category"] = get_object_or_404(Categories, slug=self.kwargs['category_slug'])
        return context


class SearchView(ListView):
    model = Articles
    template_name = "MainApp/search.html"
    context_object_name = "search_results"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('search')
        sort = self.request.GET.get('sort-by')
        if query:
            result = Articles.objects.filter(title__icontains=query) | Articles.objects.filter(content__icontains=query)
        else: result = Articles.objects.all()

        if sort or sort != '' and sort is not None:
            result = result.order_by(sort)

        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(kwargs)
        context["search_value"] = f"search={self.request.GET.get('search')}&"

        sort_value = self.request.GET.get('sort-by')
        if sort_value == 'None' or not sort_value:
            sort_value = ''
        context["sort_value"] = f"sort-by={sort_value}&"

        sort_values = []
        for value in sort_values_list:
            if value["value"] == sort_value:
                value["selected"] = "selected"
            else: value["selected"] = ""
            sort_values.append(value)
        context["sort_values_list"] = sort_values

        context["input_value"] = self.request.GET.get('search')
        return context

class CountriesView(ListView):
    template_name = "MainApp/countries.html"
    context_object_name = "countries"
    model = Region

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(kwargs)
        context["country_object"] = get_object_or_404(Region, slug=self.kwargs['country_slug'])
        all = context["country_object"].region_elements.all()
        context["articles_1"] = all[:1].first()
        context["articles_2"] = all[1:3]
        context["articles_3"] = all[3:7]
        context["articles"] = all[7:]
        context["articles_mobile"] = context["articles_2"] | context["articles_3"]
        return context



# ------------------ API VIEWSETS ------------------ #
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


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsNeuralNetUser])
def get_region_by_name(request, region_name):
    if request.method == 'GET':
        region = Region.objects.get(name=region_name)
        serializer = RegionSerializer(region)
        return Response(serializer.data)
