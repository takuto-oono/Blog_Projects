from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleList.as_view(), name='index'),
    path('detail/<int:pk>', views.ArticleDetail.as_view(), name='detail_article'),
    path('create_comment/<int:article_pk>',
         views.CreateCommentView.as_view(), name='create_comment')
]
