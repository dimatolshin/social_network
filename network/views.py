from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect

from .forms import CreateNewUser, AddPhoto
from .models import Profile, Subscription, Chat, Message, Post, Photo, Comment, Support


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
    subscribers = Subscription.objects.filter(to_subscriber=profile)[:5]
    to_subscribers = Subscription.objects.filter(subscriber=profile)[:5]
    posts = Post.objects.filter(profile=profile)
    if user_id == request.user.profile.id:
        check_element = False
    else:
        check_element = True
    subscriber = Subscription.objects.filter(to_subscriber=request.user.profile, subscriber=profile)
    if subscriber:
        subscriber = True
    return render(request, 'network/main.html',
                  {'profile': profile, 'subscribers': subscribers, 'to_subscribers': to_subscribers,
                   'check_element': check_element, 'subscriber': subscriber, 'posts': posts})


def all_subscribers(request, profile_id: int):
    profile = get_object_or_404(Profile, id=profile_id)
    subscribers = Subscription.objects.filter(to_subscriber=profile)
    return render(request, 'network/all_subscribers.html',
                  {'subscribers': subscribers, 'profile': profile})


def search_subscribers(request):
    profile = get_object_or_404(Profile, id=request.POST['profile_id'])
    username = request.POST['name_subscriber']
    if not username:
        return redirect('network:all_subscribers', request.POST['profile_id'])
    users = User.objects.filter(username__icontains=username)
    search_element = []
    subscribers = Subscription.objects.filter(to_subscriber=profile)
    for subscriber in subscribers:
        for user in users:
            if subscriber.subscriber.user == user:
                search_element += [user]

    return render(request, 'network/search_subscribers.html', {'search_element': search_element})


def all_to_subscribers(request, profile_id: int):
    profile = get_object_or_404(Profile, id=profile_id)
    to_subscribers = Subscription.objects.filter(subscriber=profile)
    return render(request, 'network/all_to_subscribers.html', {'profile': profile, 'to_subscribers': to_subscribers})


def search_to_subscribers(request):
    profile = get_object_or_404(Profile, id=request.POST['profile_id'])
    username = request.POST['name_to_subscriber']
    if not username:
        return redirect('network:all_to_subscribers', request.POST['profile_id'])
    users = User.objects.filter(username__icontains=username)
    to_subscribers = Subscription.objects.filter(subscriber=profile)
    search_element = []
    for to_subscriber in to_subscribers:
        for user in users:
            if to_subscriber.to_subscriber.user == user:
                search_element += [user]
    return render(request, 'network/search_to_subscribers.html', {'search_element': search_element})


def search_people(request):
    all_people = Profile.objects.all()
    return render(request, 'network/search_people.html', {'all_people': all_people})


def search(request):
    profiles = Profile.objects.all()
    username = request.POST['name_element']
    if not username:
        return redirect('network:search_people')
    all_people = []
    user_container = User.objects.filter(username__icontains=username)
    for user in user_container:
        for profile in profiles:
            if profile == user.profile:
                print(profile)
                all_people += [user.profile]
    return render(request, 'network/search_people.html', {'all_people': all_people})


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
        Chat.objects.create(you=request.user.profile, friend=profile)
        chats = Chat.objects.filter(you=request.user.profile, friend=profile)
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
    if not text:
        return redirect('network:message_room', chat_id)
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


def add_post(request):
    profile = get_object_or_404(Profile, id=request.POST['profile_id'])
    text = request.POST['post_text']
    if not text:
        return redirect('network:main')
    Post.objects.create(profile=profile, text=request.POST['post_text'])
    return redirect('network:main', request.POST['profile_id'])


def all_photo(request, profile_id: int):
    profile = get_object_or_404(Profile, id=profile_id)
    photos = Photo.objects.filter(profile=profile).order_by('id').reverse()
    return render(request, 'network/all_photo.html', {'photos': photos, })


def add_photo(request):
    if request.method == "POST":
        form = AddPhoto(request.POST, request.FILES)
        if form.is_valid():
            request.user.profile.photo = form.cleaned_data['picture']
            Photo.objects.create(profile=request.user.profile, picture=form.cleaned_data['picture'])
            request.user.profile.save()
            return redirect('network:main', request.user.profile.id)
    form = AddPhoto()
    return render(request, 'network/add_photo.html', {'form': form})


def detail_photo(request, photo_id: int):
    photo = get_object_or_404(Photo, id=photo_id)
    comments = Comment.objects.filter(photo=photo)
    return render(request, 'network/detail_photo.html', {'comments': comments, 'photo': photo})


def add_comment(request):
    if request.method == 'POST':
        text = request.POST['comment_text']
        if not text:
            return redirect('network:detail_photo', request.POST['photo_id'])
        photo = get_object_or_404(Photo, id=request.POST['photo_id'])
        Comment.objects.create(text=text, profile=request.user.profile, photo=photo)
    comments = Comment.objects.filter(photo=photo)
    return render(request, 'network/detail_photo.html', {'comments': comments, 'photo': photo})


def support(request):
    user_support = User.objects.get(username='Тех.Специалист')
    if not Support.objects.filter(profile=request.user.profile):
        supports = Support.objects.create(profile=request.user.profile, user_support=user_support,
                                          text='Здравствуйте, чем могу помочь?',creation_user_username='Тех.Специалист')
    supports = Support.objects.filter(profile=request.user.profile)
    return render(request, 'network/support.html', {'supports': supports})


def add_report(request):
    user_support = User.objects.get(username='Тех.Специалист')
    text = request.POST['text']
    if not text:
        return redirect('network:support')
    Support.objects.create(profile=request.user.profile, text=text, user_support=user_support,creation_user_username=request.user.username)
    return redirect('network:support')
