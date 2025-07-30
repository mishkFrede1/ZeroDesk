from django.contrib import admin
from django.utils.html import format_html

from . import models

# Register your models here.
admin.site.register(models.Tags)

@admin.register(models.Articles)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_delete_button')
    list_display_links = ('id', 'title')
    search_fields = ('title', "slug")

    def get_delete_button(self, obj):
        return format_html(f"<a style=\"color: white; font-weight: 600; padding: 4px 20px; cursor: pointer; border-radius: 8px; background-color: #FE0000;\" href='/admin/MainApp/articles/{obj.pk}/delete'>DELETE</a>")

@admin.register(models.Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')