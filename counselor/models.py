from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.text import slugify
# from comment.models import comment
from django.contrib.contenttypes.models import ContentType

from django.dispatch import receiver
from django.db.models.signals import post_save
# from django.contrib.auth.models import User
# from  .models import message

class message(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField(default='')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    writer = models.ForeignKey(User, editable=True, blank=False, null=True)


    def __str__(self):
        return self.title
    def __unicode__(self):
        return self.title
    def __str__(self):
        return self.content
    def __unicode__(self):
        return self.content

class notifications(models.Model):
    title = models.CharField(max_length=120,blank=True, null=True)
    writer = models.CharField(max_length=120,blank=False, null=True)
    message_id = models.PositiveIntegerField(blank=False, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    creator = models.CharField(max_length=120, blank=True, null=True)
    boolean_field = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title



class reply(models.Model):
    user = models.ForeignKey(User, editable=True, blank=False, null=True)
    content = models.TextField(default='')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    object_id = models.PositiveIntegerField(blank=False, null=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.content

    def __unicode__(self):
        return self.content
    def __str__(self):
        return str(self.user.username)

@receiver(post_save, sender=message)
def ensure_profile(sender, *args, **kwargs):
    var = kwargs.get('instance')
    b=notifications(title=var.title,writer=var.writer, message_id = var.pk,creator=var.writer)
    b.save()

@receiver(post_save, sender=reply)
def ensure_profile_exists(sender, *args, **kwargs):
    var = kwargs.get('instance')
    var2 = var.object_id
    var3 = message.objects.get(pk=var2)
    c=notifications(creator=var3.writer, writer=var.user, message_id = var.object_id)
    c.save()



