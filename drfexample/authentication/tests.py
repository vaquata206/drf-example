from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class RegisterInTest(TestCase):
    def setUp(self):
        self.user = {
            'username': 'admin2',
            'password': 'unknown@123',
            'password_2': 'unknown@123',
            'email': 'unknown2@gmail.com',
            'first_name': 'unknown',
            'last_name': 'unknown'
        }

        self.user_exist = {
            'username': 'admin1',
            'password': 'unknown@123',
            'email': 'unknown1@gmail.com',
            'first_name': 'unknown',
            'last_name': 'unknown'
        }

        User.objects.create_user(**self.user_exist)
        self.link_api = reverse('auth:register')

    def test_register(self):
        """register"""
        response = self.client.post(self.link_api, data=self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_exist(self):
        """case: register a user that its username is exist"""
        data = self.user_exist
        data['password_2'] = 'unknown@123'
        response = self.client.post(self.link_api, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginInTest(TestCase):
    """docstring for LoginInTest"""
    def setUp(self):
        self.user_exist = {
            'username': 'admin1',
            'password': 'unknown@123',
            'email': 'unknown1@gmail.com',
            'first_name': 'unknown',
            'last_name': 'unknown'
        }

        User.objects.create_user(**self.user_exist)
        self.link_api = reverse('auth:login')

    def test_login(self):
        data = {
            'username': 'admin1',
            'password': 'unknown@123'
        }

        response = self.client.post(self.link_api, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_fail(self):
        data = {
            'username': 'admin1',
            'password': 'unknown@1234'
        }

        response = self.client.post(self.link_api, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ChangePasswordInTest(TestCase):
    def setUp(self):
        self.user_exist = {
            'username': 'admin1',
            'password': 'unknown@123',
            'email': 'unknown1@gmail.com',
            'first_name': 'unknown',
            'last_name': 'unknown'
        }

        User.objects.create_user(**self.user_exist)

        response = self.client.post(reverse('auth:login'), data={
            'username': 'admin1',
            'password': 'unknown@123',
        })
        self.token = response.data['token']
        self.link_api = reverse('auth:change_pass')

    def test_change_password(self):
        response = self.client.post(self.link_api, data={
            'old_password': 'unknown@123',
            'new_password': 'unknown@124',
            'new_password_2': 'unknown@124'
        }, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserProfileInTest(TestCase):
    def setUp(self):
        self.user_exist = {
            'username': 'admin1',
            'password': 'unknown@123',
            'email': 'unknown1@gmail.com',
            'first_name': 'unknown',
            'last_name': 'unknown'
        }

        User.objects.create_user(**self.user_exist)
        response = self.client.post(reverse('auth:login'), data={
            'username': 'admin1',
            'password': 'unknown@123',
        })
        self.token = response.data['token']
        self.link_api = reverse('auth:user_info')

    def test_get_profile(self):
        response = self.client.get(self.link_api, HTTP_AUTHORIZATION=self.token)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_post_profile(self):
        response = self.client.post(self.link_api, HTTP_AUTHORIZATION=self.token, data={
            'first_name': 'name1',
            'last_name': 'name2',
        })

        self.assertEquals(response.status_code, status.HTTP_200_OK)
