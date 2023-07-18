from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings

from .forms import CreateNewUser, AddPhoto, EditParam
from .models import Profile, Subscription, Chat, Message, Post, Photo, Comment, Support, My_Music, All_Music


def index(request):
    return render(request, 'network/index.html')


def register(request):
    if request.method == 'POST':
        form = CreateNewUser(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно.")
            return redirect('network:main', request.user.profile.id)
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = CreateNewUser()
    return render(request, "registration/register.html", context={'form': form})


def main(request: HttpRequest, user_id: int):
    profile = get_object_or_404(Profile, id=user_id)
    subscribers = Subscription.objects.filter(to_subscriber=profile)[:5]
    to_subscribers = Subscription.objects.filter(subscriber=profile)[:5]
    posts = Post.objects.filter(profile=profile).order_by('-id')
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
    username = request.POST['name_element']
    profiles = Profile.objects.filter(user__username__icontains=username)
    if not username:
        return redirect('network:search_people')
    return render(request, 'network/search_people.html', {'all_people': profiles})

@login_required()
def add_friend(request):
    profile_id = request.POST.get('profile_id')
    profile = get_object_or_404(Profile, id=profile_id)
    subscriber = Subscription.objects.filter(to_subscriber=request.user.profile, subscriber=profile)
    if not subscriber:
        Subscription.objects.create(to_subscriber=request.user.profile, subscriber=profile)
    else:
        return redirect('network:main', profile_id)
    messages.success(request, "Вы успешно добавили друга")
    return redirect('network:main', profile_id)

@login_required()
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

@login_required()
def messanger(request):
    friend_rooms = Chat.objects.filter(friend=request.user.profile)
    my_rooms = Chat.objects.filter(you=request.user.profile)
    return render(request, 'network/messanger.html', {'my_rooms': my_rooms, 'friend_rooms': friend_rooms})

@login_required()
def message_room(request, chat_id: int):
    chat = get_object_or_404(Chat, id=chat_id)
    mess = Message.objects.filter(chat=chat).order_by('-id')
    return render(request, 'network/my_messages.html', {'mess': mess, 'chat': chat})

@login_required()
def add_message(request):
    text = request.POST['text']
    chat_id = request.POST['chat_id']
    if not text:
        return redirect('network:message_room', chat_id)
    chat = get_object_or_404(Chat, id=chat_id)
    Message.objects.create(text=text, chat=chat, author=request.user.profile)
    return redirect('network:message_room', chat_id)


def get_more_info(request):
    chat_id = int(request.GET['chat_id'])
    chat = get_object_or_404(Chat, id=request.GET[chat_id])
    messages = Message.objects.filter(chat=chat).order_by('id')
    return render(request, 'network/get_more_info.html', {'messages': messages, 'chat': chat})

@login_required()
def dell_friend(request):
    profile_id = request.POST.get('profile_id')
    profile = get_object_or_404(Profile, id=profile_id)
    subscriber = Subscription.objects.filter(to_subscriber=request.user.profile, subscriber=profile)
    subscriber.delete()
    request.user.profile.save()
    messages.success(request, "Вы удалили своего друга")
    return redirect('network:main', profile_id)

@login_required()
def add_post(request):
    profile = get_object_or_404(Profile, id=request.POST['profile_id'])
    text = request.POST['post_text']
    if not text:
        return redirect('network:main', profile.id)
    Post.objects.create(profile=profile, text=request.POST['post_text'])
    return redirect('network:main', profile.id)


def all_photo(request, profile_id: int):
    profile = get_object_or_404(Profile, id=profile_id)
    photos = Photo.objects.filter(profile=profile).order_by('-id')
    return render(request, 'network/all_photo.html', {'photos': photos, })

@login_required()
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
    comments = Comment.objects.filter(photo=photo).order_by('-id')
    return render(request, 'network/detail_photo.html', {'comments': comments, 'photo': photo})

@login_required()
def add_comment(request):
    if request.method == 'POST':
        text = request.POST['comment_text']
        if not text:
            return redirect('network:detail_photo', request.POST['photo_id'])
        photo = get_object_or_404(Photo, id=request.POST['photo_id'])
        Comment.objects.create(text=text, profile=request.user.profile, photo=photo)
    comments = Comment.objects.filter(photo=photo)
    return render(request, 'network/detail_photo.html', {'comments': comments, 'photo': photo})

@login_required()
def support(request):
    user_support = User.objects.get(username='Тех.Специалист')
    if not Support.objects.filter(profile=request.user.profile):
        Support.objects.create(profile=request.user.profile, user_support=user_support,
                                          text='Здравствуйте, чем могу помочь?',
                                          creation_user_username='Тех.Специалист')
    supports = Support.objects.filter(profile=request.user.profile).order_by('-id')
    return render(request, 'network/support.html', {'supports': supports})

@login_required()
def add_report(request):
    user_support = User.objects.get(username='Тех.Специалист')
    text = request.POST['text']
    if not text:
        return redirect('network:support')
    Support.objects.create(profile=request.user.profile, text=text, user_support=user_support,
                           creation_user_username=request.user.username)
    return redirect('network:support')

@login_required()
def add_like_picture(request):
    assert request.method == "POST"
    photo_id = request.POST['photo_id']
    photo = get_object_or_404(Photo, id=request.POST['photo_id'])
    if request.user.profile in photo.like_list.all():
        photo.like_list.remove(request.user.profile)
        photo.like -= 1
    else:
        photo.like_list.add(request.user.profile)
        photo.like += 1
    photo.save()
    return redirect('network:detail_photo', photo_id)

@login_required()
def add_like_comment(request):
    assert request.method == "POST"
    comment_id = request.POST['comment_id']
    photo = Photo.objects.get(comments__id=comment_id)
    comment = get_object_or_404(Comment, id=comment_id)
    like_data = comment.like_list.all()
    if request.user.profile in like_data:
        comment.like_list.remove(request.user.profile)
        comment.like -= 1
    else:
        comment.like_list.add(request.user.profile)
        comment.like += 1
    comment.save()
    return redirect('network:detail_photo', photo.id)

@login_required()
def add_like_post(request):
    assert request.method == "POST"
    post = get_object_or_404(Post, id=request.POST['post_id'])
    if request.user.profile in post.like_list.all():
        post.like_list.remove(request.user.profile)
        post.like -= 1
    else:
        post.like_list.add(request.user.profile)
        post.like += 1
    post.save()
    return redirect('network:main', request.user.profile.id)


def my_music(request, profile_id: int):
    profile = get_object_or_404(Profile, id=profile_id)
    musics = My_Music.objects.filter(profile=profile).order_by('id')

    return render(request, 'network/my_music.html', {'musics': musics})


def all_musics(request):
    musics = All_Music.objects.all().order_by('id')
    return render(request, 'network/all_musics.html', {'musics': musics})

@login_required()
def add_music(request):
    sound = get_object_or_404(All_Music, id=request.POST['music_id'])
    My_Music.objects.create(sound=sound, profile=request.user.profile)
    messages.success(request, 'Аудио добавлено в ваши аудиозаписи')
    return redirect('network:all_musics')

@login_required()
def delete_music(request):
    sound = My_Music.objects.filter(id=request.POST['music_id'])
    sound.delete()
    messages.success(request, 'Аудио было удалего из вашего плейлиста')
    return redirect('network:my_music', request.user.profile.id)

@login_required()
def edit_information(request):
    if request.method == "POST":
        form = EditParam(request.POST)
        if form.is_valid():
            profile = get_object_or_404(Profile, id=request.user.profile.id)
            user = request.user
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            profile.birth_date = form.cleaned_data['birth_date']
            user.save()
            profile.save()
            messages.success(request, 'Вы успешно изменили информацию')
            return redirect('network:main', profile.id)
    else:
        form = EditParam(instance=request.user)
    return render(request, 'network/edit_information.html', {'form': form})
