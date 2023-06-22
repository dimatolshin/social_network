from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect

from .models import Profile, Subscription, Chat, Message


def index(request):
    return render(request, 'network/index.html')