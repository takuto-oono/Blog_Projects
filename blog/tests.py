from django.test import TestCase
from .models import Article


class ArticleModelTests(TestCase):
    def test_is_empty(self):
        saved_articles = Article.objects.all()
        self.assertEqual(saved_articles.count(), 0)
