from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.text import slugify
from comment.models import comment
from django.contrib.contenttypes.models import ContentType


from django.dispatch import receiver
from django.db.models.signals import post_save


class post(models.Model):
    category = (
        ('career', 'career'),
        ('relationship', 'relationship'),
        ('education', 'education'),
        ('other', 'other')
    )
    option = models.CharField(max_length=20, choices=category, blank=False, null=True)
    title = models.CharField(max_length=120)
    content = models.TextField(default='')
    # slug = models.SlugField(unique=True)
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
    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"id":self.id})
    def get_url_to_list(self):
        return "/discussions/"
    @property
    def comments(self):
        instance = self
        qs = comment.objects.filter_by_instance(instance)
        return qs
    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance)
        return content_type

class notifications1(models.Model):
    title = models.CharField(max_length=120,blank=True, null=True)
    writer = models.CharField(max_length=120,blank=False, null=True)
    message_id = models.PositiveIntegerField(blank=False, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    creator = models.CharField(max_length=120, blank=True, null=True)
    boolean_field = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

@receiver(post_save, sender=comment)
def ensure_profile_exists(sender, *args, **kwargs):
    var = kwargs.get('instance')
    var2 = var.object_id
    var3 = post.objects.get(pk=var2)
    notifications1.objects.get_or_create(title=var3.title, writer=var.user, message_id=var.object_id, creator=var3.writer)







