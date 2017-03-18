from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
# from discussions.models import post
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType




class CommentManager(models.Manager):
    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id)
        return qs
class comment(models.Model):
    user = models.ForeignKey(User, editable=True, blank=False, null=True)
    content = models.TextField(default='')
    # post = models.ForeignKey(post)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(blank=False, null=True)
    objects = CommentManager()
    def __str__(self):
        return str(self.user.username)

