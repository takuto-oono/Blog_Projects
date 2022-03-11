from django.contrib import admin
from .models import Article, Comment


class ArticleAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'user',
              'is_public', 'public_date', 'good_user', 'read_later_user']


admin.site.register(Article, ArticleAdmin)


class CommentAdmin(admin.ModelAdmin):
    fields = [
        'content',
        'user',
        'article',
        'date',
        'comment_goods',
    ]


admin.site.register(Comment, CommentAdmin)
