from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

articles_router = SimpleRouter()
categories_router = SimpleRouter()
tags_router = SimpleRouter()

articles_router.register('articles', views.ArticlesViewSet, basename='articles')
categories_router.register('categories', views.CategoriesViewSet, basename='categories')
tags_router.register('tags', views.TagsViewSet, basename='tags')
urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),

    # ------------------ SITE PATHS ------------------ #
    path('article/<slug:slug>/', views.ArticleDetailView.as_view(), name='article'),
    path('tag/<slug:tag_slug>/', views.TagListView.as_view(), name='tag'),
    path('category/<slug:category_slug>/', views.CategoryListView.as_view(), name='category'),
    path('categories/', views.CategoriesListView.as_view(), name='more_categories'),
    path('latest-news/', views.LatestListView.as_view(), name='latest_news'),
    path('search/', views.SearchView.as_view(), name='search'),

    # ------------------ API ------------------ #
    path('api/v1/', include(articles_router.urls)),
    path('api/v1/', include(categories_router.urls)),
    path('api/v1/', include(tags_router.urls)),
]