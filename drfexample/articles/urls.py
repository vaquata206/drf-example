from django.conf.urls import url
from .views import ArticleListCreateAPIView, ArticleDetailUpdateAPIView, CommentCreateAPIView, CommentListAPIView

app_name = 'article'
urlpatterns = [
    url('list/', ArticleListCreateAPIView.as_view(), name='list_create'),
    url('detail/(?P<article_id>[0-9]+)/comments/', CommentListAPIView.as_view(), name='detail_comment'),
    url('detail/(?P<pk>[0-9]+)/', ArticleDetailUpdateAPIView.as_view(), name='detail'),
    url('(?P<pk>[0-9]+)/comments/', CommentCreateAPIView.as_view(), name='writing_comment'),
]
