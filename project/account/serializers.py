from rest_framework import serializers
from django.core.cache import cache
from account.models import Profile 
from article.models import Article
from django.contrib.auth.models import User

from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('ext_id', 'gravatar', 'created')

        
class UserSerializer(serializers.ModelSerializer):
    
    profile = ProfileSerializer()
    token = serializers.SerializerMethodField('generate_token')

    def generate_token(self, obj):
        print obj
        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    class Meta:
        model = User
        fields = ('username','password', 'token', 'first_name', 'last_name', 'email', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(
                username = validated_data['username'],
                password = validated_data['password'],
                email = validated_data['email'],
                first_name = validated_data['first_name'],
                last_name = validated_data['last_name']
                
            )
        p = Profile.objects.create(user = user, **profile_data)
        self._update_user_in_redis(p)
        return user

    def _update_user_in_redis(self, profile):
        cache.set(profile.ext_id, Article.objects.all(), timeout=None)
                

