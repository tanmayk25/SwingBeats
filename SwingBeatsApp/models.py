from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
import os


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    device_id = models.CharField(max_length=100, help_text="Enter the Device ID", blank = True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default = 'F')
    age = models.IntegerField(blank = True)
    weight = models.IntegerField(blank = True, help_text="Enter your weight in Kilograms")
    bio = models.TextField()

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Monitored_Detail(models.Model):
    created = models.DateTimeField(default=now, editable=False)
    device_id = models.CharField(max_length=100, help_text="Enter the Device name", blank = True)
    heart_rate = models.IntegerField(help_text="Enter the steps", default='0000000') #editable=False
    steps = models.IntegerField(help_text="Enter the calories", default='0000000')
    calories = models.IntegerField(help_text="Enter the temperature", default='0000000')
    dance_duration = models.IntegerField(help_text="Enter the dance duration", default='0000000')
    class Meta:
        ordering = [ "created"]


    def __str__(self):
        return self.device_id
