from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    #id=models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    userto = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    message = models.CharField(max_length=200)
    label=models.CharField(default='old',max_length=3)
    labelc = models.CharField(default='old', max_length=3)

    def __unicode__(self):
        return self.message

class ArchChat(models.Model):
    #id=models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    userto = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    message = models.CharField(max_length=200)

    def __unicode__(self):
        return self.message


class counsallot(models.Model):
    counsname=models.CharField(max_length=200)
    username=models.CharField(max_length=200)

    def __unicode__(self):
        return self.counsname


class requests(models.Model):
    username=models.CharField(max_length=200)
    status=models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

class notif(models.Model):
    username = models.CharField(max_length=200)
    counsname = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
