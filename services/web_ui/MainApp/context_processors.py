from django.db.models import Count
from .utils import nav
from MainApp.models import Tags, Categories

def get_nav(request):
    return {"nav": nav}

def get_popular_tags(request):
    return {"popular_tags": Tags.objects.annotate(article_count=Count('tag_elements')).order_by('-article_count')[:25]}

def get_categories(request):
    return {"categories": Categories.objects.all()[:9]}