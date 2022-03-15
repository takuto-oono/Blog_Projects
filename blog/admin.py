from django.contrib import admin
from .models import Category, Article, Comment


class CategoryAdmin(admin.ModelAdmin):
    fields = [
        'title', 'detail', 'is_public'
    ]


admin.site.register(Category, CategoryAdmin)


class ArticleAdmin(admin.ModelAdmin):
    fields = [
        'title', 'content', 'picture', 'user',
        'is_public', 'public_date', 'good_user', 'good_count', 'read_later_user', 'browsing_user']


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
