import  json

from django.views import View
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse

from .models import Music, Album, Artist, Genre, MyplaylistMusic, ArtistGenre
from account.models import User, MyPlaylist, MyFavoriteMusic
from account.utils import login_decorator

class MusicCountView(View):
    def post(self, request):
        data = json.loads(request.body)
        music_id = data['music_id']
        music = Music.objects.get(id = music_id)
        if Music.objects.filter(id = music_id).exists():
            music.play_count += 1
            music.save()
            return HttpResponse(status=200)
        return JsonResponse({'message':'INVALID_KEYS'}, status=400)

class ChartView(View):
    def get(self, request):
            charts = Music.objects.all().order_by('-play_count')
            chart100 = []
            for chart in charts:
                music_artists = chart.musicartist_set.all()
                music = Music.objects.get(name = chart.name, album_id = chart.album.id)
                artist=[]
                for music_artist in music_artists:
                    artist.append(music_artist.artist.name)
                chart_list={
                    'id'        : music.id,
                    'image_url' : chart.album.image_url,
                    'name'      : chart.name,
                    'artist'    : artist,
                    'album'     : chart.album.name,
                    'lyrics'    : chart.lyrics,
                    'select'    : False}
                chart100.append(chart_list)
            return JsonResponse({'data' : chart100}, status=200)

class MusicDetailView(View):
    def get(self,request,music_id):
        detail = Music.objects.get(id=music_id)
        artists = detail.musicartist_set.all()
        music_artist =[]
        for m in artists:
            music_artist.append(m.artist.name)
        music_detail={
            'image_url': detail.album.image_url,
            'name'     : detail.name,
            'artist'   : music_artist,
            'writer'   : detail.writer,
            'composer' : detail.composer,
            'arranger' : detail.arranger,
            'lyrics'   : detail.lyrics
        }
        return JsonResponse({'data' : music_detail}, status=200)

class StreamingView(View):
    @login_decorator
    def get(self,request):
        try:
            user = request.user
            music_id =request.GET.get('music_id', None)
            if 0< int(music_id) and int(music_id) <= len(Music.objects.all()):
                      music     = Music.objects.get(id = music_id)
                      file_name = music.sound
                      music_url = './vibemusic/' + file_name
                      content   = self.iterator(music_url)
                      response  = StreamingHttpResponse(content, status = 200)
                      response['Cache-Control'] = 'no-cache'
                      response['Content-Type'] = 'audio.mp3'
                      response['Content-Disposition'] = 'attachment; filename =' + file_name
                      response['Accept-Ranges'] = 'bytes'
                      response['Content-Length'] = len(open(music_url,'rb').read())
                      return response

            return JsonResponse({ 'message' : 'INVALID_KEYS' }, status = 400)
        
        except KeyError:
            return JsonResponse({ 'message' : 'INVALID_KEYS' }, status =400)

    def iterator(self,music_url):
        with open(music_url,'rb') as music:
            while True:
                byte = music.read()
                if byte:
                    yield byte
                else:
                    break

class MyPlaylistView(View):
    @login_decorator
    def post(self,request):
        user = request.user
        data = json.loads(request.body)
        try:
            if not MyPlaylist.objects.filter(user = user, name = data['name']).exists():
                MyPlaylist.objects.create(
                    user_id = user.id,
                    name = data['name'],
                    quantity = data['quantity']
                )
                return HttpResponse(status = 200)
            return JsonResponse({ 'message' : 'INVALID_TOKEN_OR_INVALID_NAME' }, status =400)
        
        except KeyError:
            return JsonResponse({ 'message' : 'INAVLID_KEYS' },status =400)

    @login_decorator
    def get(self,request): 
        user = request.user
        try:
            if MyPlaylist.objects.filter(user = user).exists():
                myplaylists = MyPlaylist.objects.filter(user = user)[1:]
                play_list = [{
                    'myplaylist_id': myplaylist.id,
                    'name'         : myplaylist.name,
                    'quantity'     : myplaylist.quantity,
                    'created_at'   : myplaylist.created_at
                }for myplaylist in myplaylsits]
                return HttpResponse(status =200)
            return JsonResponse({ 'message': 'INVALID_USER'}, status = 400)

        except KeyError:
            return JsonResponse({ 'message': 'INVALID_KEYS'}, status = 400)

class MyPlaylistDetailView(View):
    @login_decorator
    def get(self,request,myplaylist_id):
        try:
            user = request.user
            if MyPlaylist.objects.filter(user = user, id = myplaylist_id).exists():
                myplaylists = MyplaylistMusic.objects.filter(myplaylist_id = myplaylist_id)
                my_playlist = []
                for myplaylist in myplaylists:
                    artist = []
                    music_artists = myplaylist.music.musicartist_set.all()
                    if MyFavoriteMusic.objects.filter(music = myplaylist.music.id).exists():
                        like = True
                    else:
                        like = False
                    for music_artist in music_artists:
                        artist.append(music_artist.artist.name)
                    data = {
                        'music_id'  : myplaylist.music.id,
                        'music_name': myplaylist.music.name,
                        'image'     : myplaylist.music.album.image_url,
                        'album_name': myplaylist.music.album.name,
                        'artist'    : artist,
                        'lyrics'    : myplaylist.music.lyrics,
                        'Is_liked'  : like}
                    my_playlist.append(data)
                return JsonResponse({ 'data' : my_playlist }, status = 200)
            
            return JsonResponse({ 'message' : 'INVALID_USER_OR_INVALID_ID' }, status = 400)
        
        except KeyError:
            return JsonResponse({ 'message' : 'INVALID_KEYS' }, status =400)

class MusicAddView(View):
    @login_decorator
    def post(self,request,myplaylist_id):
        try:
            data = json.loads(request.body)
            user = request.user
            music_ids = data['music_id']
            count = 0
            if MyPlaylist.objects.filter(id = myplaylist_id,user = user).exists():
                for music_id in music_ids:
                    if not MyplaylistMusic.objects.filter(music_id = music_id).exists():
                        MyplaylistMusic.objects.create(myplaylist_id = myplaylist_id, music_id = music_id)
                        myplaylist = MyPlaylist.objects.get(id = myplaylist_id)
                        myplaylist.quantity += 1
                        myplaylist.save()
                        count += 1
                return JsonResponse({ 'count' : count }, status = 200)
                
            return JsonResponse({ 'message' : 'INVALID_VALUES' }, status = 400)
        
        except KeyError:
            return JsonResponse({ 'message' : 'INVALID_KEYS' }, status = 400)

class MusicDeleteView(view):
    @login_decorator
    def delete(self,request,myplaylist_id):
        try:
            data = json.loads(request.body)
            user = request.user
            if MyplaylistMusic.objects.filter(myplaylist__user = user, myplaylist_id = myplaylist_id, music_id = data['music_id']).exists():
                MyplaylistMusic.objects.get(myplaylist_id = myplaylist_id, music_id = data['music_id']).delete()
                return HttpResponse(status = 200)
            return JsonResponse({ 'message' : 'INVALID_VALUES' }, status = 400)

        except KeyError:
            return JsonResponse({ 'message' : 'INVALID_KEYS' }, status = 400)

class PlayerView(View):
    @login_decorator
    def get(self,request):
        try:
            user = request.user
            player = MyPlaylist.objects.filter(user = user).first()
            songs = MyplaylistMusic.objects.filter(myplaylist = player)
            player_list = []
            for song in songs:
                artist = []
                music_artists = song.music.musicartist_set.all()
                for music_artist in music_artists:
                    artist.append(music_artist.artist.name)
                data = {
                'id'        : song.music.id,
                'title'     : song.music.name,
                'urlLarge'  : song.music.album.image_url.replace('120','720'),
                'urlSmall'  : song.music.album.image_url.replace('120','100'),
                'album'     : song.music.album.name,
                'artist'    : artist,
                'lyrics'    : song.music.lyrics}
                player_list.append(data)
            return JsonResponse({ 'data' : player_list },status = 200)

        except KeyError:
            return JsonResponse({ 'message' : 'INVALID_KEYS' }, status = 400)

