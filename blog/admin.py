from django.contrib import admin
from .models import Article, Comment


class ArticleAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'create_user_id',
              'is_public', 'public_date']


admin.site.register(Article, ArticleAdmin)


class CommentAdmin(admin.ModelAdmin):
    fields = [
        'content',
        'user',
        'article',
        'date',
        'goods',
    ]


admin.site.register(Comment, CommentAdmin)
