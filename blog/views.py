from django.views.generic import ListView, DetailView
from . import models
from django.shortcuts import get_object_or_404


class ArticleList(ListView):
    template_name = 'blog/index.html'
    model = models.Article
    context_object_name = 'articles'
    queryset = models.Article.objects.filter(is_public=True)


class ArticleDetail(DetailView):
    template_name = 'blog/detail.html'
    model = models.Article
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        article = get_object_or_404(models.Article, id=self.kwargs['pk'], is_public=True)
        context.update({
            'comments': models.Comment.objects.filter(article=article)
        })
        return context

    def get_queryset(self):
        return models.Article.objects.filter(is_public=True)
