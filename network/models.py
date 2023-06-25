from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, )
    photo = models.ImageField(height_field=None, width_field=None, max_length=100,
                              default='static/media/images/default.jpg')
    birth_date = models.DateField(blank=True, auto_now=False, auto_now_add=False, null=True)

    def __str__(self):
        return self.user.username


class Subscription(models.Model):
    subscriber = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='subscribers')
    to_subscriber = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='to_subscribers')

    def __str__(self):
        return f'{self.subscriber.user.username}:{self.to_subscriber.user.username}'


class Chat(models.Model):
    name = models.CharField(max_length=100)
    profile = models.ManyToManyField(Profile, related_name='rooms', blank=True)

    def __str__(self):
        return self.profile.user.username


class Message(models.Model):
    text = models.TextField()
    date = models.DateTimeField(default=now)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='messages')
