from rest_framework import serializers
from account.models import Profile 
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('ext_id', 'gravatar', 'created')

        
class UserSerializer(serializers.ModelSerializer):
    
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'profile')
        write_only_field = ('password',)

    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(
                username = validated_data['username'],
                password = validated_data['password'],
                email = validated_data['email'],
                first_name = validated_data['first_name'],
                last_name = validated_data['last_name']
                
            )
        Profile.objects.create(user = user, **profile_data)
        return user
