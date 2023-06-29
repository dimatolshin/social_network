from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile, Subscription, Chat, Message


class SubscriberInline(admin.TabularInline):
    extra = 0
    model = Subscription
    fk_name = 'subscriber'


class ToSubscriberInline(admin.TabularInline):
    extra = 1
    model = Subscription
    fk_name = "to_subscriber"


class MessageAutorInline(admin.TabularInline):
    extra = 1
    model = Message
    fk_name = 'author'


class MessageInline(admin.TabularInline):
    extra = 1
    model = Message


class ChatYouInline(admin.TabularInline):
    extra = 0
    model = Chat
    fk_name = 'you'


class ChatFriendInline(admin.TabularInline):
    extra = 0
    model = Chat
    fk_name = 'friend'


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = [SubscriberInline, ToSubscriberInline, MessageAutorInline, ChatYouInline, ChatFriendInline]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass
