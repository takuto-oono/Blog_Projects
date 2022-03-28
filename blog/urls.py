from unicodedata import name
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('<int:category_pk>', views.ArticleList.as_view(), name='category'),
    path('', views.ArticleList.as_view(), name='index'),
    path('detail/<int:pk>', views.ArticleDetail.as_view(), name='detail_article'),
    path('create_comment/<int:article_pk>',
        views.CreateCommentView.as_view(), name='create_comment'),
    path('edit/commet/<int:pk>/<int:article_pk>/',
        views.EditComment.as_view(), name='edit_comment')
    path('delete/comment/<int:pk>', views.DeleteComment.as_view(), name='delete_comment'),
    path('do_good/<int:article_pk>', views.do_good, name='do_good'),
    path('read_later/<int:article_pk>', views.read_later, name='read_later'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
