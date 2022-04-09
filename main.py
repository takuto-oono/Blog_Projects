import os
import random
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Blog_Projects.settings')
from django import setup
import datetime

setup()

from blog.models import Category
from blog.models import Article
from blog.models import UserArticleRelationship
from blog.models import Comment
from custom_users.models import User

User_list = []
Category_list = []
Article_list = []
User_article_relationship_list = []
Comment_list = []


def create_users_detail():
    for i in range(20):
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
    public_date = datetime.datetime.now()
    for i in range(100):
        article = {
            'title': 'article-' + str(i),
            'content': 'content' + str(i),
            'user': User.objects.get(username='admin'),
            'is_public': True,
            'public_date': public_date,
            'category': Category.objects.get(title='category' + str(random.randint(0, 9))),
            'good_count': 0,
        }
        Article_list.append(article)
        public_date -= datetime.timedelta(days=4)


def register_user_article_relationship(user, article, action, date):
    User_article_relationship_list.append({
        'user': user,
        'article': article,
        'action': action,
        'date': date,
    })


def create_user_article_relationships_detail():
    for user in User.objects.all():
        date = datetime.datetime.now()
        for article in Article.objects.all():
            flag1 = random.randint(0, 2)
            if flag1 == 0:
                flag2 = random.randint(1, 2)
                if flag2 == 1:
                    register_user_article_relationship(user, article, 1, date)
                elif flag2 == 2:
                    register_user_article_relationship(user, article, 1, date)
                    register_user_article_relationship(user, article, 2, date)
            elif flag1 == 1:
                register_user_article_relationship(user, article, 3, date)

            date -= datetime.timedelta(days=random.randint(0, 3))


def create_comment_detail():
    for user in User.objects.all():
        if user.username == 'admin':
            continue
        date = datetime.datetime.now()
        for article in Article.objects.all():
            date -= datetime.timedelta(days=random.randint(0, 2))
            Comment_list.append({
                'content': str(article.title) + str(user.username),
                'article': article,
                'user': user,
                'date': date,
                'comment_goods': random.randint(0, 5)
            })



def create_users():
    for user_detail in User_list:
        user = User()
        user.username = user_detail['username']
        user.password = user_detail['password']
        print(user)
        user.save()


def create_categories():
    for category_detail in Category_list:
        category = Category()
        category.title = category_detail['title']
        category.detail = category_detail['detail']
        category.is_public = category_detail['is_public']
        print(category)
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
        print(article)
        article.save()


def create_user_article_relationships():
    for user_article_relationship_detail in User_article_relationship_list:
        user_article_relationship = UserArticleRelationship()
        user_article_relationship.user = user_article_relationship_detail['user']
        user_article_relationship.article = user_article_relationship_detail['article']
        user_article_relationship.date = user_article_relationship_detail['date']
        user_article_relationship.action = user_article_relationship_detail['action']
        print(user_article_relationship)
        user_article_relationship.save()


def create_comment():
    for comment_detail in Comment_list:
        comment = Comment()
        comment.content = comment_detail['content']
        comment.article = comment_detail['article']
        comment.user = comment_detail['user']
        comment.date = comment_detail['date']
        comment.comment_goods = comment_detail['comment_goods']
        comment.save()



def register_good_count():
    for article in Article.objects.all():
        cnt = 0
        for user_article_relationship in UserArticleRelationship.objects.all():
            if user_article_relationship.action == 2 and user_article_relationship.article == article:
                cnt += 1
        article.good_count = cnt
        print(cnt)
        article.save()


if __name__ == '__main__':
    # create_users_detail()
    # create_users()
    # print('create user')
    # time.sleep(2)
    # create_categories_detail()
    # create_categories()
    # print('create category')
    # time.sleep(2)
    # create_articles_detail()
    # create_articles()
    # print('create article')
    # time.sleep(2)
    # create_user_article_relationships_detail()
    # create_user_article_relationships()
    # print('create relationship')
    # register_good_count()
    create_comment_detail()
    create_comment()

