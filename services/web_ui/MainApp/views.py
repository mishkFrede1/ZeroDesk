from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from MainApp.models import *


# Create your views here.
def main(request):
    return HttpResponse("Hello, world.")

class IndexView(ListView):
    template_name = "MainApp/index.html"
    context_object_name = "articles"
    queryset = Articles.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(kwargs)
        context["main_article"] = context["articles"][0]
        context["vertical_article"] = context["articles"][1]
        context["side_articles"] = context["articles"][2:6]
        context["mini_articles"] = context["articles"][6:13]
        return context

class ArticleDetailView(DetailView):
    template_name = "MainApp/article.html"
    context_object_name = "article"
    slug_url_kwarg = "slug"

    def get_object(self, **kwargs):
        return get_object_or_404(Articles.objects, slug=self.kwargs['slug'])

class TagDetailView(DetailView):
    template_name = "MainApp/tag.html"
    context_object_name = "tag"
    slug_url_kwarg = "slug"

    def get_object(self, **kwargs):
        return get_object_or_404(Tags.objects, slug=self.kwargs['slug'])
