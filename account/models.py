from django.db import models
from music.models import Music, Artist, Album

class User(models.Model):
    name        = models.CharField(max_length = 50)
    email       = models.EmailField(max_length = 200)
    giftcard    = models.ForeignKey('Giftcard', on_delete = models.SET_NULL, null = True)
    artist      = models.ManyToManyField(Artist, through = 'MyFavoriteArtist')
    music       = models.ManyToManyField(Music, through = 'MyFavoriteMusic')
    album       = models.ManyToManyField(Album, through = 'MyFavoriteAlbum')
    image_url   = models.URLField(max_length = 2000)

    class Meta:
        db_table = 'users'

class MyPlaylist(models.Model):
    name        = models.CharField(max_length = 50)
    created_at  = models.DateTimeField(auto_now_add = True)
    user        = models.ForeignKey('User', on_delete = models.CASCADE)
    
    class Meta:
        db_table = 'myplaylists'

class Giftcard(models.Model):
    number      = models.CharField(max_length = 50)

    class Meta:
        db_table = 'giftcards'

class MyFavoriteArtist(models.Model):
    user        = models.ForeignKey('User', on_delete = models.CASCADE)
    artist      = models.ForeignKey(Artist, on_delete = models.CASCADE)
    
    class Meta:
        db_table = 'myfavorite_artists'

class MyFavoriteMusic(models.Model):
    user        = models.ForeignKey('User', on_delete = models.CASCADE)
    music       = models.ForeignKey(Music, on_delete = models.CASCADE)

    class Meta:
        db_table = 'myfavorite_music'

class MyFavoriteAlbum(models.Model):
    user        = models.ForeignKey('User', on_delete = models.CASCADE)
    album       = models.ForeignKey(Album, on_delete = models.CASCADE)

    class Meta:
        db_table = 'myfavorite_albums'

class Recommendation(models.Model):
    sender      = models.ForeignKey('User', on_delete = models.SET_NULL, null = True, related_name = 'sender')
    recipient   = models.ForeignKey('User', on_delete = models.SET_NULL, null = True, related_name = 'recipient')
    music       = models.ForeignKey(Music, on_delete = models.SET_NULL, null = True)
    created_at  = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        db_table = 'recommendations'

