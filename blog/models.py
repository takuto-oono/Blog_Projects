from django.db import models
from django.contrib.auth import get_user_model


class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='記事のタイトル')
    content = models.CharField(max_length=3000, verbose_name='記事内容')
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, verbose_name='編集者情報')
    PUBLIC_SETTINGS_CHOICES = (
        (False, '非公開'),
        (True, '公開中')
    )
    is_public = models.BooleanField(
        default=False, choices=PUBLIC_SETTINGS_CHOICES, verbose_name='公開設定')
    public_date = models.DateField(verbose_name='公開日')
    article_goods = models.IntegerField(default=0, verbose_name='いいね')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '記事'


class Comment(models.Model):
    content = models.CharField(max_length=1000, verbose_name='コメント内容')
    article = models.ForeignKey('Article', related_name='article', on_delete=models.CASCADE, verbose_name='対象記事')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='投稿者')
    date = models.DateField(verbose_name='公開日')
    comment_goods = models.IntegerField(default=0, verbose_name='いいね')
