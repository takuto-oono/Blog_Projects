from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'create_user_id',
              'public_settings', 'public_date']


admin.site.register(Article, ArticleAdmin)
