from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleList.as_view(), name='index'),
    path('detail/<int:pk>', views.ArticleDetail.as_view(), name='detail'),
]
