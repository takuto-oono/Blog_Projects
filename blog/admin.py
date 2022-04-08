from django.contrib import admin
from .models import Category, Article, Comment, UserArticleRelationship


class CategoryAdmin(admin.ModelAdmin):
    fields = [
        'title', 'detail', 'is_public'
    ]


admin.site.register(Category, CategoryAdmin)


class ArticleAdmin(admin.ModelAdmin):
    fields = [
        'title', 'content', 'picture', 'category', 'user',
        'is_public', 'public_date', 'good_count']


admin.site.register(Article, ArticleAdmin)


class UserArticleRelationshipAdmin(admin.ModelAdmin):
    fields = [
        'user',
        'article',
        'date',
        'action',
    ]


admin.site.register(UserArticleRelationship, UserArticleRelationshipAdmin)


class CommentAdmin(admin.ModelAdmin):
    fields = [
        'content',
        'user',
        'article',
        'date',
        'comment_goods',
    ]


admin.site.register(Comment, CommentAdmin)
