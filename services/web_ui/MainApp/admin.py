from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Articles)
admin.site.register(models.Tags)

@admin.register(models.Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')