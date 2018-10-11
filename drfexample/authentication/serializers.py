import jwt
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.compat import authenticate
from rest_framework.serializers import ModelSerializer
from rest_framework_jwt import authentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler, jwt_decode_handler


class UserLoginSerializer(ModelSerializer):
    username = serializers.CharField(required=True)
    token = serializers.CharField(read_only=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'token'
        ]

    def validate(self, data):
        password = data.get('password', None)
        username = data.get('username', None)

        user = User.objects.filter(username=username)

        if not (user.exists() and user.count() == 1):
            raise serializers.ValidationError('Username is invalid')

        user_obj = user.first()
        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError('Password is invalid')

        # payload = {
        #     'id': user_obj.id,
        #     'email': user_obj.email,
        # }
        payload = jwt_payload_handler(user_obj)

        data['token'] = 'JWT ' + jwt_encode_handler(payload)
        # data['token'] = jwt.encode(payload, settings.SECRET_KEY)
        return data


class UserRegisterSerializer(ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password_2 = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password_2',
            'email'
        ]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists')

        return value

    def validate_password(self, value):
        if len(value) < getattr(settings, 'PASSWORD_MIN_LENGTH', 8):
            raise serializers.ValidationError(
                'Password should be atleast %s characters long.' % getattr(settings, 'PASSWORD_MIN_LENGTH', 8)
            )

        return value

    def validate_password_2(self, value):
        data = self.get_initial()
        password = data.get('password')
        if password != value:
            raise serializers.ValidationError('Passwords does not match.')

        return value

    def create(self, validated_data):
        user = {
            'username': validated_data.get('username'),
            'password': validated_data.get('password'),
            'email': validated_data.get('email'),
        }

        User.objects.create_user(**user)
        return user


class ChangePasswordSerializer(ModelSerializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    new_password_2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = [
            'old_password',
            'new_password',
            'new_password_2'
        ]

    def validate_old_password(self, value):
        current_user = self.context['request'].user
        if not current_user.check_password(value):
            raise serializers.ValidationError('Password is invalid')

        return value

    def validate_new_password(self, value):
        if len(value) < getattr(settings, 'PASSWORD_MIN_LENGTH', 8):
            raise serializers.ValidationError(
                'Password should be at least %s characters long.' % getattr(settings, 'PASSWORD_MIN_LENGTH', 8)
            )

        return value

    def validate_new_password_2(self, value):
        data = self.get_initial()
        password = data.get('new_password')
        if password != value:
            raise serializers.ValidationError('Passwords does not match.')

        return value

    def update(self, instance, validated_data):
        new_password = validated_data.get('new_password')
        instance.set_password(new_password)
        instance.save()
        return instance


class UserProfileSerializer(ModelSerializer):
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'date_joined']
        read_only_fields = ('date_joined', 'username')
