import random
import string
from datetime import date
from django.test import TestCase
from .models import Article, Comment
from custom_users.models import User


class UserAssertion(TestCase):
    def User_model_test(self, user, username, password):
        self.assertEqual(user.username, username)
        self.assertEqual(user.password, password)


class ArticleAssertion(TestCase):
    def article_model_test(self, article, title, content, user, is_public, public_date, article_goods):
        self.assertEqual(article.title, title)
        self.assertEqual(article.content, content)
        self.assertEqual(article.user, user)
        self.assertEqual(article.is_public, is_public)
        self.assertEqual(article.public_date, public_date)
        self.assertEqual(article.article_goods, article_goods)


class CommentAssertion(TestCase):
    def comment_model_test(self, comment, content, article, user, date, comment_goods):
        self.assertEqual(comment.content, content)
        self.assertEqual(comment.article, article)
        self.assertEqual(comment.user, user)
        self.assertEqual(comment.date, date)
        self.assertEqual(comment.comment_goods, comment_goods)

    def comment_model_count(self, saved_comment, comment_cnt):
        self.assertEqual(saved_comment.count(), comment_cnt)


class UserModelTests(UserAssertion):
    def create_a_user_and_saving(self, username=None, password=None):
        user = User()
        if username is not None:
            user.username = username
        if password is not None:
            user.password = password
        user.save()

    def test_is_empty(self):
        saved_user = User.objects.all()
        self.assertEqual(saved_user.count(), 0)

    def test_saving_and_retrieving_user(self):
        username = 'admin'
        password = 'adminadmin'
        self.create_a_user_and_saving(username, password)
        saved_user = User.objects.all()
        self.assertEqual(saved_user.count(), 1)
        user = saved_user.first()
        self.assertEqual(username, user.username)
        self.assertEqual(password, user.password)


class ArticleModelTests(ArticleAssertion):
    def create_a_user_and_saving(self, username=None, password=None):
        user = User()
        if username is not None:
            user.username = username
        if password is not None:
            user.password = password
        user.save()

    def create_a_article_and_saving(self, title=None, content=None,
                                    user=None, is_public=None, public_date=None, article_goods=None):
        article = Article()
        if title is not None:
            article.title = title
        if content is not None:
            article.content = content
        if user is not None:
            article.user = user
        if is_public is not None:
            article.is_public = is_public
        if public_date is not None:
            article.public_date = public_date
        if article_goods is not None:
            article.article_goods = article_goods
        article.save()

    def test_is_empty(self):
        saved_article = Article.objects.all()
        self.assertEqual(saved_article.count(), 0)

    def test_saving_and_retrieving_article(self):
        username = 'admin'
        password = 'adminadmin'
        self.create_a_user_and_saving(username, password)
        title = 'test title'
        content = 'test content'
        user = User.objects.first()
        is_public = True
        public_date = date.fromisoformat('2022-01-01')
        article_goods = 5
        self.create_a_article_and_saving(title, content, user, is_public, public_date, article_goods)

        saved_article = Article.objects.all()
        self.assertEqual(saved_article.count(), 1)

        article = saved_article.first()
        self.article_model_test(article, title, content, user, is_public, public_date, article_goods)

    def test_saving_and_retrieving_articles(self):
        user_length = 100
        article_length = 10000
        user_list = []
        article_list = []
        user_register_list = [0 for _ in range(user_length)]
        t_cnt = 0

        for _ in range(user_length):
            username = create_random_string(8)
            password = create_random_string(12)
            user_list.append([username, password])

        for i in range(user_length):
            self.create_a_user_and_saving(user_list[i][0], user_list[i][1])

        print(len(user_list))
        for _ in range(article_length):
            title = create_random_string(8)
            content = create_random_string(50)
            choice = random.randrange(user_length)
            user_register_list[choice] += 1
            username = user_list[choice][0]
            user = User.objects.get(username=username)
            is_public = False
            if random.randrange(2) == 1:
                is_public = True
                t_cnt += 1

            month = str(random.randrange(12) + 1)
            if len(month) == 1:
                month = '0' + month

            day = str(random.randrange(27) + 1)
            if len(day) == 1:
                day = '0' + day

            public_date = date.fromisoformat('2022-' + month + '-' + day)

            article_goods = random.randrange(100)
            article_list.append([title, content, user, is_public, public_date, article_goods])

        for i in range(article_length):
            self.create_a_article_and_saving(article_list[i][0], article_list[i][1], article_list[i][2], article_list[i][3], article_list[i][4], article_list[i][5])

        saved_article = Article.objects.all()
        self.assertEqual(saved_article.count(), article_length)

        for i in range(article_length):
            article = Article.objects.get(title=article_list[i][0])
            self.article_model_test(article, article_list[i][0], article_list[i][1], article_list[i][2], article_list[i][3], article_list[i][4], article_list[i][5])

        for i in range(user_length):
            user = User.objects.get(username=user_list[i][0])
            article_user = Article.objects.filter(user=user)

            self.assertEqual(article_user.count(), user_register_list[i])

        public_article = Article.objects.filter(is_public=True)
        self.assertEqual(public_article.count(), t_cnt)


class CommentModelTest(CommentAssertion):
    def create_a_user_and_saving(self, username=None, password=None):
        user = User()
        if username is not None:
            user.username = username
        if password is not None:
            user.password = password
        user.save()

    def create_a_article_and_saving(self, title=None, content=None,
                                    user=None, is_public=None, public_date=None, article_goods=None):
        article = Article()
        if title is not None:
            article.title = title
        if content is not None:
            article.content = content
        if user is not None:
            article.user = user
        if is_public is not None:
            article.is_public = is_public
        if public_date is not None:
            article.public_date = public_date
        if article_goods is not None:
            article.article_goods = article_goods
        article.save()

    def create_a_comment_and_saving(self, content=None, article=None, user=None, date=None, comment_goods=None):
        comment = Comment()
        if content is not None:
            comment.content = content
        if article is not None:
            comment.article = article
        if user is not None:
            comment.user = user
        if date is not None:
            comment.date = date
        if comment_goods is not None:
            comment.comment_goods = comment_goods

        comment.save()

    def test_is_empty(self):
        self.comment_model_count(Comment.objects.all(), 0)

    def test_saving_and_retrieving_articles(self):
        user_length = 100
        article_length = 10000
        user_list = []
        article_list = []
        user_register_list = [0 for _ in range(user_length)]
        t_cnt = 0

        for _ in range(user_length):
            username = create_random_string(8)
            password = create_random_string(12)
            user_list.append([username, password])

        for i in range(user_length):
            UserModelTests.create_a_user_and_saving(user_list[i][0], user_list[i][1])

        print(len(user_list))
        for _ in range(article_length):
            title = create_random_string(8)
            content = create_random_string(50)
            choice = random.randrange(user_length)
            user_register_list[choice] += 1
            username = user_list[choice][0]
            user = User.objects.get(username=username)
            is_public = False
            if random.randrange(2) == 1:
                is_public = True
                t_cnt += 1

            month = str(random.randrange(12) + 1)
            if len(month) == 1:
                month = '0' + month

            day = str(random.randrange(27) + 1)
            if len(day) == 1:
                day = '0' + day

            public_date = date.fromisoformat('2022-' + month + '-' + day)

            article_goods = random.randrange(100)
            article_list.append([title, content, user, is_public, public_date, article_goods])

        for i in range(article_length):
            ArticleModelTests(article_list[i][0], article_list[i][1], article_list[i][2], article_list[i][3], article_list[i][4], article_list[i][5])


def create_random_string(string_len: int) -> str:
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(string_len))
