# Generated by Django 4.1.7 on 2023-07-06 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0035_alter_support_profile_alter_support_user_support'),
    ]

    operations = [
        migrations.CreateModel(
            name='All_Music',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('sound', models.FileField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='My_Music',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_musics', to='network.profile')),
                ('sound', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_musics', to='network.all_music')),
            ],
        ),
    ]