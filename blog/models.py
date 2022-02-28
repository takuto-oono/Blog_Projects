from difflib import IS_CHARACTER_JUNK
from django.db import models
from django.contrib.auth import get_user_model


class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='記事のタイトル')
    content = models.CharField(max_length=3000, verbose_name='記事内容')
    create_user_id = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, verbose_name='編集者情報')
    PUBLIC_SETTINGS_CHOICES = (
        (False, '非公開'),
        (True, '公開中')
    )
    public_settings = models.BooleanField(
        default=False, choices=PUBLIC_SETTINGS_CHOICES, verbose_name='公開設定')
    public_date = models.DateField(verbose_name='公開日')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = ('記事')
