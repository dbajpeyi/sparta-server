from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Profile(User):

    ext_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return self.name

