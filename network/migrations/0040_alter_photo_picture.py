# Generated by Django 4.1.7 on 2023-07-07 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0039_photo_like_list_post_like_list_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='picture',
            field=models.ImageField(upload_to='photo'),
        ),
    ]
