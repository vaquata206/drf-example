from rest_framework.response import Response
from rest_framework import permissions, status, views

from .serializers import UserLoginSerializer, UserRegisterSerializer, ChangePasswordSerializer, UserProfileSerializer


class LoginAPIView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class RegisterAPIView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

        return Response(serializer.data, status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(user, data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)

        return Response(serializer.data, status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(user, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)

        return Response(serializer.data, status.HTTP_400_BAD_REQUEST)
