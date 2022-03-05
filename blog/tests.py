from django.test import TestCase
from blog.models import Article, Comment
from custom_users.models import User
from datetime import date
from django.db import IntegrityError, transaction



class ArticleModelTests(TestCase):
    def create_user(self, username, password):
        user = User()
        user.username = username
        user.password = password
        user.save()

    def create_article(self, title, content, user, is_public, public_date, article_goods):

        try:
            with transaction.atomic():
                article = Article()
                article.title = title
                article.content = content
                article.user = user
                article.is_public = is_public
                article.public_date = public_date
                article.article_goods = article_goods
                article.save()
        except IntegrityError:
            pass


    def test_is_empty(self):
        saved_article = Article.objects.all()
        self.assertEqual(saved_article.count(), 0)

    def test_is_count_one(self):
        username = 'admin'
        password = 'password'
        self.create_user(username, password)
        title = 'title'
        content = 'content'
        user = User.objects.get(username=username)
        is_public = True
        public_date = date.fromisoformat('2022-01-24')
        article_good = 5
        self.create_article(title, content, user, is_public, public_date, article_good)
        saved_article = Article.objects.all()
        article = Article.objects.get(title=title)
        self.assertEqual(saved_article.count(), 1)
        self.assertEqual(article.title, title)
        self.assertEqual(article.content, content)
        self.assertEqual(article.user, user)
        self.assertEqual(article.is_public, is_public)
        self.assertEqual(article.public_date, public_date)
        self.assertEqual(article.article_goods, article_good)

    def test_is_no_same_title(self):
        username = 'admin'
        password = 'password'
        self.create_user(username, password)
        title1 = 'title'
        content1 = 'content1'
        user = User.objects.get(username=username)
        is_public1 = True
        public_date1 = date.fromisoformat('2022-01-24')
        article_good1 = 5
        self.create_article(title1, content1, user, is_public1, public_date1, article_good1)

        title2 = 'title'
        content2 = 'content2'
        is_public2 = False
        public_date2 = date.fromisoformat('2019-12-21')
        article_good2 = 0
        self.create_article(title2, content2, user, is_public2, public_date2, article_good2)
        saved_articles = Article.objects.all()
        print(saved_articles.count())
        self.assertEqual(saved_articles.count(), 1)
        self.assertEqual(saved_articles.first().content, content1)
