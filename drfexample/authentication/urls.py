from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from .views import LoginAPIView, RegisterAPIView, ChangePasswordAPIView, UserProfileAPIView


app_name = 'auth'
urlpatterns = [
    url('get-token/', obtain_jwt_token),
    url('login/', LoginAPIView.as_view(), name='login'),
    url('register/', RegisterAPIView.as_view(), name='register'),
    url('change-password/', ChangePasswordAPIView.as_view(), name='change_pass'),
    url('user-info/', UserProfileAPIView.as_view(), name='user_info')
]
