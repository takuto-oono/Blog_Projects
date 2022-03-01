from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . import models


class ArticleList(ListView):
    template_name = 'blog/index.html'
    model = models.Article
    context_object_name = 'articles'
    queryset = models.Article.objects.filter(public_settings=True)


class ArticleDetail(DetailView):
    template_name = 'blog/detail.html'
    model = models.Article
    context_object_name = 'article'
    queryset = models.Article.objects.filter(public_settings=True)