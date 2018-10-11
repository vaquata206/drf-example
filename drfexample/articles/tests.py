from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from .models import Article


class CommentInTest(TestCase):
    def setUp(self):
        user = {
            'username': 'admin1',
            'password': 'unknown@123',
            'email': 'unknown1@gmail.com',
            'first_name': 'unknown',
            'last_name': 'unknown'
        }

        user_obj = User.objects.create_user(**user)

        article = {
            'title': 'title3',
            'description': 'description3',
            'body': 'body3',
            'author': user_obj
        }

        article_obj = Article(**article)
        article_obj.save()

        self.link = reverse('article:writing_comment', kwargs={'pk': article_obj.id})

    def test_write_comment(self):
        data = {
            'body': 'hello'
        }
        response = self.client.post(self.link, data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)


class ArticleInTest(TestCase):
    def setUp(self):

        # To create a user
        user = {
            'username': 'admin1',
            'password': 'unknown@123',
            'email': 'unknown1@gmail.com',
            'first_name': 'unknown',
            'last_name': 'unknown'
        }
        user_obj = User.objects.create_user(**user)

        # To create a article
        article = {
            'title': 'title3',
            'description': 'description3',
            'body': 'body3',
            'author': user_obj
        }
        article_obj = Article(**article)
        article_obj.save()

        # Get the user's token
        payload = jwt_payload_handler(user_obj)
        self.token = 'JWT ' + jwt_encode_handler(payload)

        self.list_create_link = reverse('article:list_create')
        self.detail_link = reverse('article:detail', kwargs={'pk': article_obj.id})

    def test_showing_article_list(self):
        response = self.client.get(self.list_create_link)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_posting_article(self):
        article = {
            'title': 'title4',
            'description': 'description4',
            'body': 'body4',
        }
        response = self.client.post(self.list_create_link, data=article, HTTP_AUTHORIZATION=self.token)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_view_detail(self):
        response = self.client.get(self.detail_link)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_update_article(self):
        response = self.client.patch(self.detail_link, data={
            'title': 'title4',
            'description': 'description5',
            'body': 'body5',
        }, HTTP_AUTHORIZATION=self.token, content_type='application/x-www-form-urlencoded')

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_permission_update_article(self):
        other_user = {
            'username': 'admin2',
            'password': 'unknown@123',
            'email': 'unknown2@gmail.com',
            'first_name': 'unknown',
            'last_name': 'unknown'
        }
        other_user_obj = User.objects.create_user(**other_user)

        payload = jwt_payload_handler(other_user_obj)
        token = 'JWT ' + jwt_encode_handler(payload)

        response = self.client.patch(self.detail_link, data={
            'title': 'title4',
            'description': 'description5',
            'body': 'body5',
        }, HTTP_AUTHORIZATION=token, content_type='application/x-www-form-urlencoded')

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
