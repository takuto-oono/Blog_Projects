from django.views.generic import ListView, DetailView, CreateView
from . import models
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse


class ArticleList(ListView):
    template_name = 'blog/index.html'
    model = models.Article

    def get_good_article_list(self):
        good_article_list = []
        for article in models.Article.objects.filter(is_public=True).order_by('-public_date', '-good_count'):
            if self.request.user in article.good_user.all():
                good_article_list.append(article)

        return good_article_list

    def get_later_article_list(self):
        read_later_list = []
        for article in models.Article.objects.filter(is_public=True).order_by('-public_date', '-good_count'):
            if self.request.user in article.read_later_user.all():
                read_later_list.append(article)
        return read_later_list

    def get_context_data(self, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)
        context.update({
            'article_list': models.Article.objects.filter(is_public=True).order_by('-public_date', '-good_count'),
            'good_article_list': self.get_good_article_list(),
            'read_later_list': self.get_later_article_list()
        })
        return context


class ArticleDetail(DetailView):
    template_name = 'blog/detail.html'
    model = models.Article

    def write_browsing_history(self, reading_article):
        user = self.request.user
        if user not in reading_article.browsing_user.all():
            reading_article.browsing_user.add(user)

    def get_recommended_article_list(self):
        recommended_article_list = []
        for article in models.Article.objects.filter(is_public=True).order_by('-good_count', '-public_date'):
            if self.request.user not in article.browsing_user.all():
                recommended_article_list.append(article)
        return recommended_article_list

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        article = get_object_or_404(models.Article, id=self.kwargs['pk'], is_public=True)
        self.write_browsing_history(article)
        context.update({
            'comments': models.Comment.objects.filter(article=article),
            'good_cnt': article.good_user.all().count(),
            'recommend_article_list': self.get_recommended_article_list(),
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


def do_good(request, article_pk):
    article = models.Article.objects.get(pk=article_pk)
    user = request.user
    if user in article.good_user.all():
        article.good_user.remove(user)
        article.good_count -= 1
    else:
        article.good_user.add(user)
        article.good_count += 1

    article.save()
    return redirect('detail_article', article_pk)


def read_later(request, article_pk):
    article = models.Article.objects.get(pk=article_pk)
    user = request.user
    if user in article.read_later_user.all():
        article.read_later_user.remove(user)
    else:
        article.read_later_user.add(user)

    return redirect('detail_article', article_pk)
