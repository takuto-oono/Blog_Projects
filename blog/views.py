from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView
from . import models
from django.shortcuts import get_object_or_404, redirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import JsonResponse
from datetime import datetime


# read: 1
# good: 2
# later: 3

class ArticleList(ListView):
    template_name = 'blog/index.html'
    model = models.Article
    paginate_by = 12

    def create_title(self, **kwargs):
        if self.kwargs:
            if 'category_pk' in self.kwargs:
                return models.Category.objects.get(pk=self.kwargs['category_pk'])
            if 'user_mode' in self.kwargs:
                mode = self.kwargs['user_mode']
                if mode == 1:
                    title = '閲覧履歴'
                elif mode == 2:
                    title = '高評価記事'
                elif mode == 3:
                    title = '後で読むリスト'
                return title
        else:
            return 'ホーム'

    def get_queryset(self, **kwargs):
        if self.kwargs:
            if 'category_pk' in self.kwargs:
                queryset = models.Article.objects.filter(
                    is_public=True, category=models.Category.objects.get(pk=self.kwargs['category_pk']))
                return queryset.order_by('-public_date', '-good_count')
            if 'user_mode' in self.kwargs:
                if not self.request.user.is_authenticated:
                    raise Http404("この機能はログインをしないと使えません。")
                mode = self.kwargs['user_mode']
                queryset = models.UserArticleRelationship.objects.order_by('-date').filter(
                    user=self.request.user,
                    action=mode).values(
                    'article__title',
                    'article__content',
                    'article',
                    'article__picture',
                    'article__public_date',
                    'date',
                    'article__category',

                )

                return queryset
        else:
            queryset = models.Article.objects.filter(is_public=True)
            return queryset.order_by('-public_date', '-good_count')

    def get_recommended_article_list(self):
        recommended_article_list = []
        articles = models.Article.objects.filter(
            is_public=True).order_by('-good_count', '-public_date')
        read_article_list = []
        if self.request.user.is_authenticated:
            user_article_relationships = models.UserArticleRelationship.objects.filter(user=self.request.user, action=1)
            cnt = 0
            for user_article_relationship in user_article_relationships:
                read_article_list.append(user_article_relationship.article)
            for article in articles:
                if article in read_article_list:
                    continue
                cnt += 1
                recommended_article_list.append(article)
                if cnt >= 10:
                    break
            return recommended_article_list
        else:
            cnt = 0
            for article in articles:
                recommended_article_list.append(article)
                cnt += 1
                if cnt == 10:
                    break
            return recommended_article_list
        # for article in models.Article.objects.filter(is_public=True).order_by('-public_date', '-good_count'):
        #     if self.request.user in article.read_later_user.all():
        #         read_later_list.append(article)
        # return read_later_list

    def create_is_mode(self, **kwargs):
        if 'user_mode' in self.kwargs:
            return self.kwargs['user_mode']
        return 0

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super(ArticleList, self).get_context_data(**kwargs)
            context.update({
                'category_list': models.Category.objects.filter(is_public=True),
                'recommended_article_list': self.get_recommended_article_list(),
                'is_mode': self.create_is_mode(**kwargs),
                'title': self.create_title(**kwargs),
            })
            return context
        else:
            context = super(ArticleList, self).get_context_data(**kwargs)
            context.update({
                'category_list': models.Category.objects.filter(is_public=True),
                'recommended_article_list': self.get_recommended_article_list(),
                'is_mode': 0,
                'title': self.create_title(**kwargs),
            })
            # context = {
            #     'category_list': models.Category.objects.filter(is_public=True),
            #     'recommended_article_list': self.get_recommended_article_list(),
            #     'is_mode': False,
            #     'title': self.create_title(**kwargs),
            # }
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
        return context


class ArticleDetail(DetailView):
    template_name = 'blog/detail.html'
    model = models.Article

    # @method_decorator(login_required)
    def write_browsing_history(self, reading_article):
        if self.request.user:
            user = self.request.user
            if models.UserArticleRelationship.objects.filter(article=reading_article, user=user, action=1):
                user_article_relationship = models.UserArticleRelationship.objects.get(article=reading_article,
                                                                                       user=user, action=1)
                user_article_relationship.date = datetime.now()
                user_article_relationship.save()
            else:
                new_user_article_relationship = models.UserArticleRelationship()
                new_user_article_relationship.article = reading_article
                new_user_article_relationship.user = user
                new_user_article_relationship.date = datetime.now()
                new_user_article_relationship.action = 1
                new_user_article_relationship.save()

    # @method_decorator(login_required)
    def get_later_article_list(self):
        read_later_list = []
        if self.request.user.is_authenticated:
            for user_article_relationship in models.UserArticleRelationship.objects.filter(user=self.request.user,
                                                                                           action=3).order_by('date'):
                read_later_list.append(user_article_relationship.article)
            return read_later_list
        else:
            articles = models.Article.objects.filter(
                is_public=True).order_by('-good_count', '-public_date')
            cnt = 0
            for article in articles:
                read_later_list.append(article)
                cnt += 1
                if cnt == 10:
                    break
            return read_later_list

        # for article in articles:
        #     if self.request.user in article.read_later_user.all():
        #         recommended_article_list.append(article)
        # for article in articles:
        #     if self.request.user not in article.browsing_user.all() and article not in recommended_article_list:
        #         recommended_article_list.append(article)
        # for article in articles:
        #     if self.request.user in article.browsing_user.all() and article not in recommended_article_list:
        #         recommended_article_list.append(article)
        # return recommended_article_list

        # for article in models.Article.objects.filter(is_public=True).order_by('-public_date', '-good_count'):
        #     if self.request.user in article.read_later_user.all():
        #         read_later_list.append(article)
        # return read_later_list

    def get_is_good(self, article):
        if not self.request.user.is_authenticated:
            return '高評価する'
        if models.UserArticleRelationship.objects.filter(user=self.request.user, article=article, action=2).count() > 0:
            return '高評価を外す'
        else:
            return '高評価する'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        article = get_object_or_404(
            models.Article, id=self.kwargs['pk'], is_public=True)
        if self.request.user.is_authenticated:
            self.write_browsing_history(article)
            context.update({
                'comments': models.Comment.objects.filter(article=article),
                'good_cnt': article.good_count,
                'good_button_value': self.get_is_good(article),
                'later_article_list': self.get_later_article_list(),
                'category_list': models.Category.objects.filter(is_public=True),
            })
        else:
            context.update({
                'comments': models.Comment.objects.filter(article=article),
                'good_cnt': article.good_count,
                'good_button_value': '高評価する',
                'later_article_list': self.get_later_article_list(),
                'category_list': models.Category.objects.filter(is_public=True),

            })

        return context

    def get_queryset(self):
        return models.Article.objects.filter(is_public=True)


def get_good_count_ajax(request, article_pk):
    good_count = models.Article.objects.get(pk=article_pk).good_count
    return JsonResponse({'good_count': good_count})


class ShowBrowsingHistory(LoginRequiredMixin, ListView):
    login_url = '/account/login'
    REDIRECT_FIELD_NAME = 'next'
    template_name = 'blog/show_browsing_history.html'
    model = models.UserArticleRelationship
    paginate_by = 10

    def get_queryset(self):
        queryset = models.UserArticleRelationship.objects.filter(user=self.request.user).order_by('date')
        return queryset


class ShowUserComment(LoginRequiredMixin, ListView):
    login_url = '/account/login'
    REDIRECT_FIELD_NAME = 'next'
    template_name = 'blog/show_comment.html'
    model = models.Comment

    def get_queryset(self):
        queryset = models.Comment.objects.filter(user=self.request.user)
        return queryset


class CreateCommentView(LoginRequiredMixin, CreateView):
    login_url = '/account/login'
    REDIRECT_FIELD_NAME = 'next'
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
        form.date = datetime.now()
        form.save()

        return super().form_valid(form)


class EditComment(LoginRequiredMixin, UpdateView):
    login_url = '/account/login'
    REDIRECT_FIELD_NAME = 'next'
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
            form.date = datetime.now()
            form.save()
            return super().form_valid(form)
        else:
            raise Http404('編集権限がありません')


# class DeleteComment(DeleteView, LoginRequiredMixin):
#     template_name = 'blog/delete_comment.html'
#     model = models.Comment
#
#     def get_object(self, queryset=None):
#         obj = super(DeleteComment, self).get_object()
#         if not obj.user == self.request.user:
#             raise Http404
#         return obj
#
#     def get_success_url(self, **kwargs) -> str:
#         return reverse('detail_article', kwargs={'pk': self.kwargs['article_pk']})
#
#     def get_context_data(self, **kwargs):
#         context = super(DeleteComment, self).get_context_data(**kwargs)
#         context['article_pk'] = self.kwargs['article_pk']
#         return context


@login_required
def delete_comment_ajax(request):
    comment_pk = request.POST.get('comment_pk')
    comment = models.Comment.objects.get(pk=comment_pk)
    if comment.user == request.user:
        comment.delete()
        response = {
            'message': 'このコメントを削除しました。'
        }
    else:
        response = {
            'message': 'このコメントは削除できません。'
        }
    return JsonResponse(response)


# @login_required
def do_good_ajax(request, article_pk):
    article = models.Article.objects.get(pk=article_pk)
    if not request.user.is_authenticated:
        response = {
            'good_count': article.good_count,
            'is_good': False,
            'is_redirect': True
        }
        return JsonResponse(response)
    user = request.user
    if models.UserArticleRelationship.objects.filter(user=user, article=article, action=2).count() == 1:
        user_article_relationship = models.UserArticleRelationship.objects.get(user=user, article=article, action=2)
        user_article_relationship.delete()
        article.good_count -= 1
        response = {
            'good_count': article.good_count,
            'is_good': False,
            'is_redirect': False
        }
        article.save()
    else:
        new_user_article_relationship = models.UserArticleRelationship()
        new_user_article_relationship.user = user
        new_user_article_relationship.article = article
        new_user_article_relationship.action = 2
        new_user_article_relationship.date = datetime.now()
        article.good_count += 1
        response = {
            'good_count': article.good_count,
            'is_good': True,
            'is_redirect': False
        }
        new_user_article_relationship.save()
        article.save()

    return JsonResponse(response)


# @login_required
def read_later_ajax(request):
    article = models.Article.objects.get(pk=request.POST.get('article_pk'))
    if not request.user.is_authenticated:
        response = {
            'read_later': False,
            'is_redirect': True,
        }
        return JsonResponse(response)
    user = request.user
    if models.UserArticleRelationship.objects.filter(article=article, user=user, action=3):
        user_article_relationship = models.UserArticleRelationship.objects.get(article=article, user=user, action=3)
        user_article_relationship.delete()
        response = {
            'read_later': False,
            'is_redirect': False,
        }
    else:
        new_user_article_relationship = models.UserArticleRelationship()
        new_user_article_relationship.user = user
        new_user_article_relationship.article = article
        new_user_article_relationship.action = 3
        new_user_article_relationship.date = datetime.now()
        new_user_article_relationship.save()
        response = {
            'read_later': True,
            'is_redirect': False,
        }

    return JsonResponse(response)


def get_all_is_read_later(request):
    if not request.user.is_authenticated:
        response = {
            'is_authenticated': False
        }
        return JsonResponse(response)
    read_later_list = []
    for user_article_relationship in models.UserArticleRelationship.objects.filter(user=request.user, action=3):
        read_later_list.append(user_article_relationship.article.pk)
    response = {
        'is_authenticated': True,
        'read_later_list': read_later_list,
    }
    return JsonResponse(response)


def get_category_title_ajax(request):
    print('get category title ajax')
    category_pk = request.GET.get('category_pk')
    if models.Category.objects.filter(pk=category_pk):
        response = {
            'category_title': models.Category.objects.get(pk=category_pk).title
        }
        return JsonResponse(response)
    else:
        return JsonResponse({'category_title': ''})
