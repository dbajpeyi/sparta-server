import hashlib 
from django.conf import settings

def GRAVATAR_URL(email,size=200):
    m = hashlib.md5()
    email = email.strip().lower()
    m.update(email)
    return "%s%s?size="% (GRAVATAR_URL, m.hexdigest(), size) 
