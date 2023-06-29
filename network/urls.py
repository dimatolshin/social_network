from django.urls import path

from . import views

app_name = "network"

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('main/<int:user_id>', views.main, name='main'),
    path('add_fiend/', views.add_friend, name='add_friend'),
    path('check_chat/', views.check_chat, name='check_chat'),
    path('messanger/', views.messanger, name='messanger'),
    path('messanger/<int:chat_id>', views.message_room, name='message_room'),
    path('add_message', views.add_message, name='add_message'),
    path('dell_friend',views.dell_friend, name='dell_friend'),
]
