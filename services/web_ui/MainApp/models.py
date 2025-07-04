from django.db import models
from django.urls import reverse


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

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article", kwargs={"slug": self.slug})

    class Meta:
        verbose_name_plural = 'Articles'
        ordering = ['-created_at']

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