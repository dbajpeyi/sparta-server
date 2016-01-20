from __future__ import unicode_literals

from django.db import models
import uuid

# Create your models here.


class Article(models.Model):
    """
    Model to keep articles
    """
    ext_id = models.UUIDField(primary_key=True, db_index=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, unique=True, db_index=True)
    content = models.TextField()   
    author = models.CharField(max_length=50, blank=True, null=True)
    posted_on= models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s by %s" % (self.head, self.author)
