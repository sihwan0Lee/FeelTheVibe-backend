# Generated by Django 3.0.7 on 2020-06-12 04:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='album',
            field=models.ManyToManyField(through='account.MyFavoriteAlbum', to='music.Album'),
        ),
        migrations.AddField(
            model_name='user',
            name='artist',
            field=models.ManyToManyField(through='account.MyFavoriteArtist', to='music.Artist'),
        ),
        migrations.AddField(
            model_name='user',
            name='giftcard',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Giftcard'),
        ),
        migrations.AddField(
            model_name='user',
            name='music',
            field=models.ManyToManyField(through='account.MyFavoriteMusic', to='music.Music'),
        ),
        migrations.AddField(
            model_name='recommendation',
            name='music',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='music.Music'),
        ),
        migrations.AddField(
            model_name='recommendation',
            name='recipient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recipient', to='account.User'),
        ),
        migrations.AddField(
            model_name='recommendation',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sender', to='account.User'),
        ),
        migrations.AddField(
            model_name='myplaylist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.User'),
        ),
        migrations.AddField(
            model_name='myfavoritemusic',
            name='music',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Music'),
        ),
        migrations.AddField(
            model_name='myfavoritemusic',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.User'),
        ),
        migrations.AddField(
            model_name='myfavoriteartist',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Artist'),
        ),
        migrations.AddField(
            model_name='myfavoriteartist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.User'),
        ),
        migrations.AddField(
            model_name='myfavoritealbum',
            name='album',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Album'),
        ),
        migrations.AddField(
            model_name='myfavoritealbum',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.User'),
        ),
    ]
