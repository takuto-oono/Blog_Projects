from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime


class Category(models.Model):
    title = models.CharField(
        max_length=50, verbose_name='カテゴリーのタイトル', unique=True
    )
    detail = models.CharField(
        max_length=1000, verbose_name='カテゴリーについて'
    )
    PUBLIC_SETTINGS_CHOICES = (
        (False, '非公開'),
        (True, '公開中')
    )
    is_public = models.BooleanField(
        default=False, choices=PUBLIC_SETTINGS_CHOICES, verbose_name='公開設定')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'カテゴリー'


class Article(models.Model):
    title = models.CharField(
        max_length=50, verbose_name='記事のタイトル', unique=True)
    content = models.CharField(max_length=3000, verbose_name='記事内容')
    picture = models.ImageField(null=True, blank=True, default='article_thumbnail/default.JPG',
                                upload_to='article_thumbnail', verbose_name='記事のサムネ')
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, verbose_name='編集者情報', related_name='create_user')
    PUBLIC_SETTINGS_CHOICES = (
        (False, '非公開'),
        (True, '公開中')
    )
    is_public = models.BooleanField(
        default=False, choices=PUBLIC_SETTINGS_CHOICES, verbose_name='公開設定')
    public_date = models.DateField(verbose_name='更新日', default=datetime.now)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='カテゴリー', null=True, blank=True)
    good_user = models.ManyToManyField(
        get_user_model(), blank=True, verbose_name='高評価ユーザー', related_name='good_user')
    good_count = models.IntegerField(default=0, verbose_name='いいねの数')
    read_later_user = models.ManyToManyField(get_user_model(), blank=True, verbose_name='後で読むユーザー',
                                             related_name='later_user')
    browsing_user = models.ManyToManyField(get_user_model(), blank=True, related_name='browsing_user',
                                           verbose_name='閲覧したユーザー')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '記事'


class UserArticleRelationship(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, verbose_name='ユーザー')
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, verbose_name='記事')
    public_date = models.DateField(verbose_name='活動日', default=datetime.now)
    action = models.IntegerField(default=0, verbose_name='活動内容')

    def __str__(self):
        return str(self.user.username) + ':' + str(self.article.title)

    class Meta:
        verbose_name_plural = '活動内容'


class Comment(models.Model):
    content = models.CharField(max_length=1000, verbose_name='コメント内容')
    article = models.ForeignKey(
        'Article', related_name='article', on_delete=models.CASCADE, verbose_name='対象記事')
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, verbose_name='投稿者')
    date = models.DateField(
        verbose_name='更新日', default=datetime.now)
    comment_goods = models.IntegerField(default=0, verbose_name='いいね')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = 'コメント'
