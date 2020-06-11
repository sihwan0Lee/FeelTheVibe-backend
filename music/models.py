from django.db import models

class Album(models.Model):
    name            = models.CharField(max_length = 50)
    image_url       = models.URLField(max_length = 2000)
    description     = models.TextField()
    release_date    = models.DateField(null = True)
    created_at      = models.DateTimeField(auto_now_add= True)

    class Meta:
        db_table = 'albums'

class Music(models.Model):
    name        = models.CharField(max_length = 50)
    album       = models.ForeignKey('Album', on_delete = models.SET_NULL, null = True)
    sound       = models.URLField(max_length = 2000)
    playtime    = models.TimeField(null = True)
    play_count  = models.IntegerField(null = True, default = 0)
    lyrics      = models.TextField()
    is_title    = models.BooleanField()
    artist      = models.ManyToManyField('Artist', through = 'MusicArtist')
    staff       = models.ManyToManyField('Staff', through = 'MusicStaff')
    myplaylist  = models.ManyToManyField('account.MyPlaylist', through = 'MyPlaylistMusic')
    
    class Meta:
        db_table = 'music'

class Genre(models.Model):
    name        = models.CharField(max_length = 50)

    class Meta:
        db_table = 'genres'

class Artist(models.Model):
    name        = models.CharField(max_length = 50)
    debut_date  = models.DateField(null = True)
    image_url   = models.URLField(max_length = 2000)
    genre       = models.ManyToManyField('Genre',through = 'ArtistGenre')
    
    class Meta:
        db_table = 'artists'

class ArtistGenre(models.Model):
    artist      = models.ForeignKey('Artist', on_delete = models.CASCADE)
    genre       = models.ForeignKey('Genre', on_delete = models.CASCADE)
    
    class Meta:
        db_table = 'artist_genres'

class MusicArtist(models.Model):
    music       = models.ForeignKey('Music', on_delete = models.CASCADE)
    artist      = models.ForeignKey('Artist', on_delete = models.CASCADE)
    
    class Meta:
        db_table = 'music_artists'

class MyplaylistMusic(models.Model):
    myplaylist  = models.ForeignKey('account.Myplaylist', on_delete = models.CASCADE)
    music       = models.ForeignKey('Music', on_delete = models.CASCADE)

    class Meta:
        db_table = 'myplaylist_music'

class Theme(models.Model):
    name        = models.CharField(max_length = 50)

    class Meta:
        db_table = 'themes'

class DjStation(models.Model):
    theme       = models.ForeignKey('Theme', on_delete = models.SET_NULL, null = True)
    image_url   = models.URLField(max_length = 2000)
    music       = models.ForeignKey('Music', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'dj_stations'

class Staff(models.Model):
    name        = models.CharField(max_length = 50)
    staff_type  = models.ForeignKey('StaffType', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'staffs'

class StaffType(models.Model):
    name        = models.CharField(max_length = 50)

    class Meta:
        db_table = 'staff_types'

class MusicStaff(models.Model):
    music       = models.ForeignKey('Music', on_delete = models.CASCADE)
    staff       = models.ForeignKey('Staff', on_delete = models.CASCADE)

    class Meta:
        db_table = 'music_staffs'

