import os
import random
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Blog_Projects.settings')
from django import setup
from datetime import date

setup()

from blog.models import Category
from blog.models import Article
from custom_users.models import User

User_list = []
Category_list = []
Article_list = []


def create_users_detail():
    for i in range(10):
        user = {
            'username': 'username' + str(i),
            "password": 'password' + str(i),
        }
        User_list.append(user)


def create_categories_detail():
    for i in range(10):
        category = {
            'title': 'category' + str(i),
            'detail': 'detail' + str(i),
            'is_public': True,
        }
        Category_list.append(category)


def create_articles_detail():
    for i in range(30):
        article = {
            'title': 'article-' + str(i),
            'content': 'content' + str(i),
            'user': User.objects.get(username='username' + str(random.randint(0, 9))),
            'is_public': True,
            'public_date': date.fromisoformat('2022-01-01'),
            'category': Category.objects.get(title='category' + str(random.randint(0, 9))),
            'good_count': 0,
        }
        Article_list.append(article)


def create_users():
    for user_detail in User_list:
        user = User()
        user.username = user_detail['username']
        user.password = user_detail['password']
        user.save()


def create_categories():
    for category_detail in Category_list:
        category = Category()
        category.title = category_detail['title']
        category.detail = category_detail['detail']
        category.is_public = category_detail['is_public']
        category.save()


def create_articles():
    for article_detail in Article_list:
        article = Article()
        article.title = article_detail['title']
        article.content = article_detail['content']
        article.user = article_detail['user']
        article.is_public = article_detail['is_public']
        article.public_date = article_detail['public_date']
        article.good_count = article_detail['good_count']
        article.category = article_detail['category']
        article.save()


if __name__ == '__main__':
    create_users_detail()
    create_users()
    time.sleep(5)
    create_categories_detail()
    create_categories()
    time.sleep(5)
    create_articles_detail()
    create_articles()
