from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, )
    photo = models.ImageField(default='/photo/default.jpg', upload_to='photo')
    birth_date = models.DateField(blank=True, auto_now=False, auto_now_add=False, null=True)

    def __str__(self):
        return self.user.username


class Subscription(models.Model):
    subscriber = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='subscribers')
    to_subscriber = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='to_subscribers')

    def __str__(self):
        return f'{self.subscriber.user.username}:{self.to_subscriber.user.username}'


class Chat(models.Model):
    you = models.ForeignKey(Profile, related_name='you_room', on_delete=models.CASCADE, )
    friend = models.ForeignKey(Profile, related_name='friend_room', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.you.user.username}:{self.friend.user.username}'


class Message(models.Model):
    text = models.TextField()
    date = models.DateTimeField(default=now)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author')

    def __str__(self):
        return f'{self.author.user.username}:{self.text}'


class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='post')
    text = models.TextField()
    data = models.DateField(default=now)
    like_list = models.ManyToManyField(Profile, related_name='like_posts')
    like = models.IntegerField(default=0)

    def __str__(self):
        return self.profile.user.username


class Photo(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='photos')
    picture = models.ImageField(upload_to='photo')
    like_list = models.ManyToManyField(Profile, related_name='like_photos')
    like = models.IntegerField(default=0)

    def __str__(self):
        return self.profile.user.username


class Comment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    like_list = models.ManyToManyField(Profile, related_name='like_comments')
    like = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.profile.user.username}:{self.text}'


class Support(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='support')
    user_support = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support', blank=True)
    text = models.TextField()
    creation_user_username = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.user_support.username} : {self.profile.user.username}'


class All_Music(models.Model):
    name = models.CharField(max_length=100)
    sound = models.FileField(upload_to='music')

    def __str__(self):
        return self.name


class My_Music(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='my_musics')
    sound = models.ForeignKey(All_Music, on_delete=models.CASCADE, related_name='my_musics')

    def __str__(self):
        return f'{self.profile.user.username}:{self.sound.name}'
