from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import Article, Comment


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff']


class CommentSerializer(ModelSerializer):
    body = serializers.CharField(required=True)

    class Meta:
        model = Comment
        fields = ['id', 'body', 'createdOnDate', 'article']
        read_only_fields = ('id', 'createdOnDate', 'article')


class ArticleSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)

    def get_comments(self, obj):
        query = Comment.objects.filter(article_id=obj.id)[:5]
        serializer = CommentSerializer(query, many=True)
        return serializer.data

    class Meta:
        model = Article
        fields = ['id', 'title', 'description', 'body', 'createdOnDate', 'author', 'comments', 'image']
        read_only_fields = ('createdOnDate', 'id',)
