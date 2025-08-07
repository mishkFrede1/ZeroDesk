from django.db import models
from django.urls import reverse
from django.core.cache import cache


class Articles(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    summary = models.TextField()
    image = models.ImageField(upload_to='article_images/%Y/%m/%d/')
    content = models.TextField()
    category = models.ForeignKey('Categories', on_delete=models.CASCADE, related_name='category_elements')
    tags = models.ManyToManyField('Tags', related_name='tag_elements')
    likes_count = models.IntegerField(default=0)
    dislikes_count = models.IntegerField(default=0)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    region = models.ForeignKey('Region', null=True, blank=True, on_delete=models.SET_NULL, related_name='region_elements')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article", kwargs={"slug": self.slug})

    def delete(self, *args, **kwargs):
        cache.delete(f"zerodesk_article:{self.slug}")
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Articles'
        ordering = ['-created_at']


class Region(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("region", kwargs={"slug": self.slug})


class Categories(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", kwargs={"category_slug": self.slug})

    class Meta:
        verbose_name_plural = 'Categories'


class Tags(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tag", kwargs={"tag_slug": self.slug})

    class Meta:
        verbose_name_plural = 'Tags'