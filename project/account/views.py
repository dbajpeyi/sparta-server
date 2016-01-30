from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from account.serializers import UserSerializer 
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class CreateUserView(CreateAPIView):

    model = User 
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer





class LikedArticleCountView(APIView):
    def get(self, request, format=None):
        user = get_user_from(request)
        count = ArticleAction.objects.filter(profile=user, is_liked=True).count()
        return Response({'count' : count})

        




