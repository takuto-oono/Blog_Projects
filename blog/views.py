from django.views.generic import ListView, DetailView, CreateView
from . import models
from django.shortcuts import get_object_or_404
from django.urls import reverse


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


class CreateCommentView(CreateView):
    template_name = 'blog/create_comment.html'
    model = models.Comment
    fields = ['content']

    def get_success_url(self, **kwargs):
        return reverse('detail_article', kwargs={'pk': self.kwargs['article_pk']})

    def form_valid(self, form, **kwargs):
        form = form.save(commit=False)
        form.article = models.Article.objects.get(pk=self.kwargs['article_pk'])
        form.user = self.request.user
        form.save()

        return super().form_valid(form)
