from django.urls import path
from . import views
urlpatterns = [
    path('', views.IndexView.as_view(), name='root'),
    path('article/<slug:slug>/', views.ArticleDetailView.as_view(), name='article'),
    path('tag/<slug:slug>/', views.TagDetailView.as_view(), name='tag'),
]