from django.urls import path

from . import views

app_name = "network"

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('main/<int:user_id>/', views.main, name='main'),
    path('add_fiend/', views.add_friend, name='add_friend'),
    path('check_chat/', views.check_chat, name='check_chat'),
    path('messanger/', views.messanger, name='messanger'),
    path('messanger/<int:chat_id>', views.message_room, name='message_room'),
    path('add_message/', views.add_message, name='add_message'),
    path('dell_friend/', views.dell_friend, name='dell_friend'),
    path('add_post/', views.add_post, name='add_post'),
    path('all_subscribers/<int:profile_id>/', views.all_subscribers, name='all_subscribers'),
    path('search_subscribers/', views.search_subscribers, name='search_subscribers'),
    path('all_to_subscribers/<int:profile_id>/', views.all_to_subscribers, name='all_to_subscribers'),
    path('search_to_subscribers/', views.search_to_subscribers, name='search_to_subscribers'),
    path('all_photo/<int:profile_id>/', views.all_photo, name='all_photo'),
    path('add_photo/', views.add_photo, name='add_photo'),
    path('detail_photo/<int:photo_id>/', views.detail_photo, name='detail_photo'),
    path('search_people/', views.search_people, name='search_people'),
    path('search/', views.search, name='search'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('support/', views.support, name='support'),
    path('add_report/', views.add_report, name='add_report'),
    path('add_like_picture/', views.add_like_picture, name='add_like_picture'),
    path('add_like_comment', views.add_like_comment, name='add_like_comment'),
    path('add_like_post', views.add_like_post, name='add_like_post'),
    path('my_musics/<int:profile_id>/', views.my_music, name='my_music'),
    path('all_musics/', views.all_musics, name='all_musics'),
    path('add_music/', views.add_music, name='add_music'),
    path('delete_music/', views.delete_music, name='delete_music'),
    path('edit_information', views.edit_information, name='edit_information')
]
