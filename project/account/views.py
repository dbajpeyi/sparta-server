from django.shortcuts import render
from account.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from article.serializers import ProfileSerializer


class CreateProfile(APIView):

    def post(self, request, format=None):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(
                serializer.init_data['email'],
                serializer.init_data['username'],
                serializer.init_data['password']
            )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



