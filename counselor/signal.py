from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from  .models import message

@receiver(post_save, sender=message)
def ensure_profile_exists(sender, **kwargs):
    print ("it is working")