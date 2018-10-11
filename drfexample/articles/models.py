import uuid
from django.contrib.auth.models import User
from django.db import models


class Article(models.Model):
    def image_directory_path(self, filename):
        index_dot = filename.rfind('.')
        if index_dot < 0:
            raise ValueError('filename is invalid')

        extension = filename[index_dot:]
        return 'image/' + uuid.uuid4().hex + extension

    title = models.CharField(max_length=100)
    description = models.TextField()
    body = models.TextField()

    author = models.ForeignKey(
        User, related_name='author_article', on_delete=models.CASCADE
    )

    image = models.FileField(blank=True, null=True, upload_to=image_directory_path)

    createdOnDate = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    body = models.TextField()
    createdOnDate = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(
        Article, related_name='comments', on_delete=models.CASCADE
    )
