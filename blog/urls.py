from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleList.as_view(), name='index'),
    path('detail/<int:pk>', views.ArticleDetail.as_view(), name='detail_article'),
    path('create_comment/<int:article_pk>',
         views.CreateCommentView.as_view(), name='create_comment'),
    path('do_good/<int:article_pk>', views.do_good, name='do_good'),
    path('read_later/<int: article_pk>', views.read_later, name='read_later'),
]
