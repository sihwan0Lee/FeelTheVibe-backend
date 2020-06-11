import os
import django
import csv
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE','vibe_main.settings')
django.setup()

from music.models import  *


def create_genre():
    genres = ['발라드','댄스','팝락','뮤지컬','랩/힙합','일렉트로니카','알앤비/어반','인디뮤직','락','팝','포크','드라마음악','얼터너티브 락','캐롤','트로트','알앤비','힙합']
    for genre in genres:
        Genre.objects.create(name=genre)

def create_album():
        
    CSV_PATH_PRODUCT = '../vibe.csv'

    with open(CSV_PATH_PRODUCT) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader,None)

        for row in data_reader:
            if row:
                album_image = row[0]
                album_name = row[12]
                album_desc = row[16]
                release_date = row[14].replace('.','-')
                if "데뷔" in row[10]:
                    debut = row[10]
                else:
                    debut = ''
                if not Album.objects.filter(name = album_name).exists():
                    Album.objects.create(name = album_name, image_url = album_image, description = album_desc,release_date = release_date)

    # artist 데이터 
def create_artist():
    CSV_PATH_PRODUCT = '../vibe1.csv'

    with open(CSV_PATH_PRODUCT) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader,None)

        for row in data_reader:
            if row:
                name = row[0]
                image = row[3]
                if "데뷔" in row[1]:
                    debut = row[1]
                else:
                    debut = ''
                if "데뷔" in row[2]:
                    terminator = row[2].index('뷔')
                    genre = row[2][terminator+1:]
                else:
                    genre = row[2]
                genres = genre.split(', ')
                if not Artist.objects.filter(name = row[0]).exists():
                    Artist.objects.create(name = name, debut_date = debut, image_url = image)




def create_artist_genre():
    CSV_PATH_PRODUCT = '../vibe1.csv'

    with open(CSV_PATH_PRODUCT) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader,None)

        for row in data_reader:
            if row:
                name = row[0]
                image = row[3]
                if "데뷔" in row[1]:
                    debut = row[1]
                else:
                    debut = ''
                if "데뷔" in row[2]:
                    terminator = row[2].index('뷔')
                    genre = row[2][terminator+1:]
                else:
                    genre = row[2]
                genres = genre.split(', ')
                for g in genres:
                    if not ArtistGenre.objects.filter(artist_id = Artist.objects.get(name=row[0]).id, genre_id = Genre.objects.get(name = g).id).exists():
                        ArtistGenre.objects.create( artist = Artist.objects.get(name = row[0]), genre = Genre.objects.get(name = g))

def create_music():
    CSV_PATH_PRODUCT = '../vibe.csv'
    
    with open(CSV_PATH_PRODUCT) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader,None)
        
        for row in data_reader:
            if row:
                name = row[2]
                album = Album.objects.get(name = row[12])
                lyrics = row[7]
                is_title = 1
                writer = row[4]
                composer = row[5]
                arranger = row[6]
                Music.objects.create(name = name,album = album, lyrics = lyrics,is_title = 1, writer = writer, composer = composer, arranger = arranger)

def create_music_artist():
    CSV_PATH_PRODUCT = '../vibe2.csv'
    
    with open(CSV_PATH_PRODUCT) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader,None)
        for row in data_reader:
            if row:
                music_name = row[2]
                artist_name = row[8]
                album_id = Album.objects.get(name = row[12]).id
                MusicArtist.objects.create(music = Music.objects.get(name = music_name,album_id=album_id),artist = Artist.objects.get(name = row[8]))



#create_genre()
#create_album()
#create_artist()
#create_artist_genre()
#create_music()
#create_music_artist()
