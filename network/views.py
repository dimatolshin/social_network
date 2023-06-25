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


def main(request, user_id: int):
    profile = get_object_or_404(Profile, id=user_id)
    subscribers = Subscription.objects.filter(to_subscriber=profile)
    to_subscribers = Subscription.objects.filter(subscriber=profile)
    print(subscribers)
    print(to_subscribers)
    return render(request, 'network/main.html',
                  {'profile': profile, 'subscribers': subscribers, 'to_subscribers': to_subscribers})
