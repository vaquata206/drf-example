from rest_framework import permissions, status, views, generics, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ArticleSerializer, CommentSerializer
from .models import Article, Comment
from .permissions import IsOwnerPermission
from .paginations import StandardResultSetPagination


class CommentCreateAPIView(views.APIView):

    permission_classes = (permissions.AllowAny,)
    serializer_class = CommentSerializer

    def post(self, request, pk=None):
        try:
            article = Article.objects.filter(pk=pk)
            if article.count() == 0:
                raise ValueError('The article is not exist')
            article_obj = article.first()
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        comment = serializer.validated_data
        serializer.save(article=article_obj, body=comment['body'])
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentListAPIView(views.APIView):

    permission_classes = (permissions.AllowAny,)
    serializer_class = CommentSerializer
    pagination_class = StandardResultSetPagination

    def get(self, request, article_id=None):
        comments = Comment.objects.filter(article_id=article_id).order_by('id')
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            result = self.get_paginated_response(serializer.data)
            return result

        serializer = self.serializer_class(comments, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class ArticleListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = ArticleSerializer
    queryset = Article.objects.select_related('author')
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('title', 'body')
    filter_fields = ('title', 'body', 'author__username')
    pagination_class = StandardResultSetPagination

    def perform_create(self, serializer):
        current_user = self.request.user
        serializer.save(author=current_user)


class ArticleDetailUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerPermission)
    serializer_class = ArticleSerializer
    queryset = Article.objects.select_related('author')
