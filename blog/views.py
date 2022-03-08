from django.views.generic import ListView, DetailView
from . import models


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
        article = models.Article.objects.get(id=self.kwargs['pk'])
        context.update({
            'comments': models.Comment.objects.filter(article=article)
        })
        return context

    def get_queryset(self):
        return models.Article.objects.filter(is_public=True)
