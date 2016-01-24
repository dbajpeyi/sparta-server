from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from account.serializers import UserSerializer 
from django.contrib.auth.models import User


class CreateUserView(CreateAPIView):

    model = User 
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer

