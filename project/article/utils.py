
from account.models import Profile 
from django.contrib.auth.models import User
from rest_framework_jwt.authentication import jwt_decode_handler
from rest_framework_jwt.authentication import jwt_get_username_from_payload 
from rest_framework.authentication import get_authorization_header


def get_user_from(request):

    auth = get_authorization_header(request).split()[1]
    payload = jwt_decode_handler(auth)
    username = jwt_get_username_from_payload(payload)
    return _get_user_for(username)

def _get_user_for(username):
    return Profile.objects.get(user = User.objects.get(username = username))


