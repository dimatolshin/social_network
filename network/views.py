from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect

from .forms import CreateNewUser
from .models import Profile, Subscription, Chat, Message


def index(request):
    return render(request, 'network/index.html')


def register(request):
    if request.method == 'POST':
        form = CreateNewUser(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('network:index')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = CreateNewUser()
    return render(request, "registration/register.html", context={'form': form})


def main(request: HttpRequest, user_id: int):
    profile = get_object_or_404(Profile, id=user_id)
    subscribers = Subscription.objects.filter(to_subscriber=profile)
    to_subscribers = Subscription.objects.filter(subscriber=profile)
    if user_id == request.user.profile.id:
        check_element = False
    else:
        check_element = True
    subscriber = Subscription.objects.filter(to_subscriber=request.user.profile, subscriber=profile)
    if subscriber:
        subscriber = True
    # TOD Subscription.objects (если есть друг то кнока удалить )
    return render(request, 'network/main.html',
                  {'profile': profile, 'subscribers': subscribers, 'to_subscribers': to_subscribers,
                   'check_element': check_element, 'subscriber': subscriber})


def add_friend(request):
    profile_id = request.POST.get('profile_id')
    profile = get_object_or_404(Profile, id=profile_id)
    subscriber = Subscription.objects.filter(to_subscriber=request.user.profile, subscriber=profile)
    if not subscriber:
        Subscription.objects.create(to_subscriber=request.user.profile, subscriber=profile)
    else:
        return redirect('network:main', profile_id)
    return redirect('network:main', profile_id)


def check_chat(request):
    profile_id = request.POST.get('profile_id')
    profile = get_object_or_404(Profile, id=profile_id)
    chats = Chat.objects.filter(you=request.user.profile, friend=profile)
    if not chats:
        chats = Chat.objects.filter(friend=request.user.profile, you=profile)
    if not chats:
        chats = Chat.objects.create(you=request.user.profile, friend=profile)
    for chat in chats:
        chat_id = chat.id
    return redirect('network:message_room', chat_id)


def messanger(request):
    friend_rooms = Chat.objects.filter(friend=request.user.profile)
    my_rooms = Chat.objects.filter(you=request.user.profile)
    return render(request, 'network/messanger.html', {'my_rooms': my_rooms, 'friend_rooms': friend_rooms})


def message_room(request, chat_id: int):
    chat = get_object_or_404(Chat, id=chat_id)
    messages = Message.objects.filter(chat=chat)
    return render(request, 'network/my_messages.html', {'messages': messages, 'chat': chat})


def add_message(request):
    text = request.POST['text']
    chat_id = request.POST['chat_id']
    chat = get_object_or_404(Chat, id=chat_id)
    Message.objects.create(text=text, chat=chat, author=request.user.profile)
    return redirect('network:message_room', chat_id)


def dell_friend(request):
    profile_id = request.POST.get('profile_id')
    profile = get_object_or_404(Profile, id=profile_id)
    subscriber = Subscription.objects.filter(to_subscriber=request.user.profile, subscriber=profile)
    subscriber.delete()
    request.user.profile.save()
    return redirect('network:main', profile_id)
