import http.client
from re import T
from sysconfig import is_python_build
from unicodedata import category
from urllib import request

from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from . import forms
from . import models
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
import datetime
from django import http
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.http import JsonResponse


class CategoryList(ListView):
    template_name = 'blog/category.html'
    model = models.Category

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        context.update({
            'article_list': models.Article.objects.filter(is_public=True,
                                                          category=models.Category(pk=self.kwargs['category_pk'])),
        })


class ArticleList(ListView):
    template_name = 'blog/index.html'
    model = models.Article
    paginate_by = 10

    def get_queryset(self, **kwargs):
        if self.kwargs:
            queryset = models.Article.objects.filter(
                is_public=True, category=models.Category.objects.get(pk=self.kwargs['category_pk']))
            return queryset.order_by('-public_date', '-good_count')
        else:
            queryset = models.Article.objects.filter(is_public=True)
            return queryset.order_by('-public_date', '-good_count')

    # def get_queryset(self, **kwargs):
    #     queryset = models.Article.objects.all.filter(is_public=True)
    #     queryset = super().get_queryset()
    #     print(models.Article.objects.filter(category=models.Category.objects.get(pk=25)))
    #     if self.kwargs:
    #         print(self.kwargs['category_pk'])
    #         print(models.Article.objects.filter(category=models.Category.objects.get(pk=self.kwargs['category_pk'])))
    #         queryset.filter(category=models.Category.objects.get(pk=self.kwargs['category_pk']))
    #         print(queryset)
    #     else:
    #         queryset.filter(is_public=True)
    #     return queryset.order_by('-public_date', '-good_count')

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
            'category_list': models.Category.objects.filter(is_public=True),
            'good_article_list': self.get_good_article_list(),
            'read_later_list': self.get_later_article_list(),
        })
        return context


class CategoryDetail(TemplateView):
    template_name = 'blog/category.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        category = models.Category.objects.get(
            pk=self.kwargs['category_pk'], is_public=True)
        context.update({
            'article_list': models.Article.objects.filter(is_public=True, category=category)
        })
        print(context)
        return context


class ArticleDetail(DetailView):
    template_name = 'blog/detail.html'
    model = models.Article

    # @method_decorator(login_required)
    def write_browsing_history(self, reading_article):
        if self.request.user:
            user = self.request.user
            if user not in reading_article.browsing_user.all():
                reading_article.browsing_user.add(user)

    # @method_decorator(login_required)
    def get_recommended_article_list(self):
        recommended_article_list = []
        articles = models.Article.objects.filter(
            is_public=True).order_by('-good_count', '-public_date')
        for article in articles:
            if self.request.user in article.read_later_user.all():
                recommended_article_list.append(article)
        for article in articles:
            if self.request.user not in article.browsing_user.all() and article not in recommended_article_list:
                recommended_article_list.append(article)
        for article in articles:
            if self.request.user in article.browsing_user.all() and article not in recommended_article_list:
                recommended_article_list.append(article)
        return recommended_article_list

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        article = get_object_or_404(
            models.Article, id=self.kwargs['pk'], is_public=True)
        if self.request.user.is_authenticated:
            self.write_browsing_history(article)
            context.update({
                'comments': models.Comment.objects.filter(article=article),
                'good_cnt': article.good_count,
                'recommend_article_list': self.get_recommended_article_list(),
                'category_list': models.Category.objects.filter(is_public=True)
            })
        else:
            context.update({
                'comments': models.Comment.objects.filter(article=article),
                'good_cnt': article.good_count,

            })

        return context

    def get_queryset(self):
        return models.Article.objects.filter(is_public=True)


def get_good_count_ajax(request, article_pk):

    good_count = models.Article.objects.get(pk=article_pk).good_count

    return JsonResponse({'good_count': good_count})

# class DeleteArticle(DeleteView):
#     model = models.Article
#     success_url = '/admin_admin/'
#     def get_success_url(self):
#     return reverse('admin_article_list')

# def delete(self, request, *args, **kwargs):
#     self.object = self.get_object()
#     if self.object.user == self.request.user:
#         self.object.delete()
#         return http.HttpResponseRedirect(self.success_url)
#     else:


class CreateCommentView(CreateView, LoginRequiredMixin):
    template_name = 'blog/create_comment.html'
    model = models.Comment
    fields = ['content']

    def get_context_data(self, **kwargs):
        context = super(CreateCommentView, self).get_context_data(**kwargs)
        context['article_content'] = models.Article.objects.get(
            pk=self.kwargs['article_pk'])
        return context

    def get_success_url(self, **kwargs):
        return reverse('detail_article', kwargs={'pk': self.kwargs['article_pk']})

    def form_valid(self, form, **kwargs):
        form = form.save(commit=False)
        form.article = models.Article.objects.get(pk=self.kwargs['article_pk'])
        form.user = self.request.user
        form.save()

        return super().form_valid(form)


class EditComment(UpdateView, LoginRequiredMixin):
    template_name = 'blog/edit_comment.html'
    model = models.Comment
    fields = ['content']

    def get_context_data(self, **kwargs):
        context = super(EditComment, self).get_context_data(**kwargs)
        context['article_content'] = models.Article.objects.get(
            pk=self.kwargs['article_pk'])
        return context

    def get_success_url(self, **kwargs):
        return reverse('detail_article', kwargs={'pk': self.kwargs['article_pk']})

    def form_valid(self, form):
        form = form.save(commit=False)
        if form.user == self.request.user:
            form.save()
            return super().form_valid(form)
        else:
            raise Http404('編集権限がありません')


class DeleteComment(DeleteView, LoginRequiredMixin):
    template_name = 'blog/delete_comment.html'
    model = models.Comment

    def get_object(self, queryset=None):
        obj = super(DeleteComment, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def get_success_url(self, **kwargs) -> str:
        return reverse('detail_article', kwargs={'pk': self.kwargs['article_pk']})

    def get_context_data(self, **kwargs):
        context = super(DeleteComment, self).get_context_data(**kwargs)
        context['article_pk'] = self.kwargs['article_pk']
        return context


@login_required
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


@login_required
def read_later(request, article_pk):
    article = models.Article.objects.get(pk=article_pk)
    user = request.user
    if user in article.read_later_user.all():
        article.read_later_user.remove(user)
    else:
        article.read_later_user.add(user)

    return redirect('index')
