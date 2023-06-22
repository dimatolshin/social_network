from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    photo = models.ImageField(height_field=None, width_field=None, max_length=100, blank=True)
    birth_date = models.DateField(blank=True)

    def __str__(self):
        return self.user.username


class Subscription(models.Model):
    subscriber = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='subscribers')
    to_subscribe = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='to_subscribers')


    def __str__(self):
        return self.subscriber.user.username

class Chat(models.Model):
    name = models.CharField(max_length=100)
    profiles = models.ManyToManyField(Profile, related_name='rooms', blank=True)

    def __str__(self):
        return self.profiles.user.username


class Message(models.Model):
    text = models.TextField()
    date = models.DateTimeField(default=now)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='messages')

