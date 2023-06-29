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
    # TODO Subscription.objects (если есть друг то кнока удалить )
    return render(request, 'network/main.html',
                  {'profile': profile, 'subscribers': subscribers, 'to_subscribers': to_subscribers,
                   'check_element': check_element})


def add_friend(request):
    profile_id = request.POST['profile_id']
    profile = get_object_or_404(Profile, id=profile_id)
    Subscription.objects.create(to_subscriber=request.user.profile, subscriber=profile)
    return redirect('network:main', profile_id)


def add_chat(request):
    profile_id = request.POST['profile_id']
    profile = get_object_or_404(Profile, id=profile_id)
    chat = request.user.profile.rooms.filter(name=profile.user.username)
    if not chat:
        chat = request.user.profile.rooms.create(profile=profile, name=profile.user.username)
    return redirect('network:messanger') #TODO redirect ('massage_room' ,chat.id)


def messanger(request):
    all_rooms = request.user.profile.rooms.all()
    return render(request, 'network/messanger.html', {'all_rooms': all_rooms})


def message_room(request,chat_id):
    pass
