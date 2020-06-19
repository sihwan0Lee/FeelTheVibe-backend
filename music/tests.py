import json
from music.models  import Music,Album,Artist,MusicArtist
from django.test   import TestCase, Client
from unittest.mock import patch, MagicMock

class ChartTest(TestCase):
    def setUp(self):
        Album.objects.create(
            id = '1',
            name = '집8',
            image_url = 'http://domain.com/?image_name=name'
            )

        Artist.objects.create(
            id = '1',
            name = 'choi'
            )

        Music.objects.create(
            id = '1',
            album_id = '1',
            name = '12',
            sound = '12',
            lyrics = '123123',
            is_title = 'True',
            arranger = '22'
            )
        
        MusicArtist.objects.create(
            music = Music.objects.get(id=1),
            artist = Artist.objects.get(id=1)
            )
    def tearDown(self):
        Music.objects.all().delete()
        Album.objects.all().delete()
        Artist.objects.all().delete()
        MusicArtist.objects.all().delete()
    
    def test_chart(self):
        c = Client()

        
        response = c.get('/music/chart', {'content_type':'application/json'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'data' :[
                { 
                'id' : 1,
                'image_url' : 'http://domain.com/?image_name=name',
                'name' : '12',
                'artist' : ['choi'],
                'album' : '집8',
                'lyrics' : '123123',
                'select' : False

                }]})



class DetailTest(TestCase):
    def setUp(self):
        Album.objects.create(
            id = '1',
            name = '집9',
            image_url = 'http://domain.com/?image_name=name'
            )
        
        Artist.objects.create(
            id = '1',
            name = 'lee'
            )
        
        Music.objects.create(
            id = '1',
            album_id = '1',
            name = 'hi',
            writer = 'qw',
            composer = '123ed',
            arranger = 'gkgkgk',
            lyrics = 'fowijhgoiegjo',
            is_title = 'True'
            )
        MusicArtist.objects.create(
            music = Music.objects.get(id=1),
            artist = Artist.objects.get(id=1)
            )
    def tearDown(self):
        Music.objects.all().delete()
        Album.objects.all().delete()
        Artist.objects.all().delete()
        MusicArtist.objects.all().delete()

    def test_detail(self):
        c = Client()

        response = c.get('/music/detail/1', {'content_type':'application/json'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'data' :{
            'image_url' : 'http://domain.com/?image_name=name' ,
            'name' : 'hi',
            'artist' : 'lee',
            'writer' : 'qw',
            'composer' : '123ed',
            'arranger' : 'gkgkgk',
            'lyrics' : 'fowijhgoiegjo'
            }})
