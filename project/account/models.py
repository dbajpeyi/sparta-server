from __future__ import unicode_literals
import hashlib 

from django.db import models
from django.contrib.auth.models import User
import uuid
from endpoints import GRAVATAR_URL

# Create your models here.

class Profile(models.Model):

    ext_id  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user    = models.OneToOneField(User)
    gravatar= models.URLField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.gravatar:
            self.gravatar = self.gravatar_url(100)
        super(Profile, self).save(*args, **kwargs)


    def gravatar_url(self, size):
        if self.email:
            return GRAVATAR_URL(self.email)

