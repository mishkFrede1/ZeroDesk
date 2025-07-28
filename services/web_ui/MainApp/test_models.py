from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from MainApp.models import Categories, Articles, Tags

def create_test_article():
    category = Categories.objects.create(name="Category", slug="category")
    tag = Tags.objects.create(name="Tag", slug="tag")
    image = SimpleUploadedFile(
        name="image.jpg",
        content=b'\x47\x49\x46\x38\x89\x61',
        content_type="image/jpeg",
    )

    article = Articles.objects.create(
        title="Title1",
        slug="slug1",
        summary="Summary1",
        content="Content1",
        category=category,
        image=image
    )
    article.tags.set([tag])
    article.save()
    return article

class TestArticles(TestCase):
    def setUp(self):
        create_test_article()

    def test_get_absolute_url(self):
        article = Articles.objects.get(slug="slug1")
        self.assertEqual(article.get_absolute_url(), "/article/slug1/")

    def test_default_fields(self):
        article = Articles.objects.get(slug="slug1")
        self.assertEqual(article.is_published, False)

    def test_valid_create(self):
        article = Articles.objects.get(slug="slug1")
        self.assertEqual(article.category.name, "Category")
        self.assertEqual(article.tags.first().name, "Tag")
        self.assertEqual(article.image.url[:39]+article.image.url[46:], "/media/article_images/2025/07/28/image_.jpg")


class TestCategories(TestCase):
    def setUp(self):
        create_test_article()
        Categories.objects.create(name="Category1", slug="category1")
        Categories.objects.create(name="Category2", slug="category2")

    def test_get_absolute_url(self):
        category1 = Categories.objects.get(name="Category1")
        category2 = Categories.objects.get(name="Category2")
        self.assertEqual(category1.get_absolute_url(), "/category/category1/")
        self.assertEqual(category2.get_absolute_url(), "/category/category2/")

    def test_article_category_relation(self):
        article = Articles.objects.get(slug="slug1")
        category = Categories.objects.get(slug="category")
        self.assertEqual(article.category.name, category.name)


class TestTags(TestCase):
    def setUp(self):
        create_test_article()
        Tags.objects.create(name="Tag1", slug="tag1")
        Tags.objects.create(name="Tag2", slug="tag2")

    def test_get_absolute_url(self):
        tag1 = Tags.objects.get(name="Tag1")
        tag2 = Tags.objects.get(name="Tag2")
        self.assertEqual(tag1.get_absolute_url(), "/tag/tag1/")
        self.assertEqual(tag2.get_absolute_url(), "/tag/tag2/")

    def test_article_category_relation(self):
        article = Articles.objects.get(slug="slug1")
        tag = Tags.objects.get(slug="tag")
        self.assertEqual(article.tags.first().name, tag.name)