from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Articles)
admin.site.register(models.Categories)
admin.site.register(models.Tags)