import jwt
import json
import requests
import bcrypt

from django.views import View
from django.http  import JsonResponse,HttpResponse

from vibe_main.settings  import SECRET_KEY, HASH
from .models import User, MyPlaylist, MyFavoriteMusic
from .utils import login_decorator
from music.models import Music,Album, Artist, MyplaylistMusic

class NaverSocialSignInView(View):
    def get(self, request):
        naver_s_token = request.headers.get('Authorization', None)
        header = {'Authorization':f"Bearer {naver_s_token}"}

        url = 'https://openapi.naver.com/v1/nid/me'
        response = requests.get(url, headers=header, timeout=3)
        user_info = response.json()

        try:
            if User.objects.filter(email = user_info['response']['email']).exists():
                user = User.objects.get(email = user_info['response']['email'])
                token = jwt.encode({"email":user_info['response']['email']},SECRET_KEY, algorithm = HASH).decode('utf-8')
                return JsonResponse({"token" : token, "nickname" : user.nickname, "image" : user.image_url}, status = 200)

            else:
                User(
                    name = user_info['response']["name"],
                    nickname = user_info['response']["nickname"],
                    image_url = user_info['response']["profile_image"],
                    email = user_info['response']["email"]
                    ).save()
                user = User.objects.get(email = user_info['response']['email'])
                token = jwt.encode({ "email" : user_info['response']['email'] }, SECRET_KEY, algorithm = HASH).decode('utf-8')
                return JsonResponse({ "token" : token, "nickname" : user.nickname, "image" : user.image_url }, status = 200)
        
        except  KeyError as e:
            return JsonResponse({ "message" : "INVALID_KEYS" }, status = 400)

class MyFavoriteMusicView(View):
    @login_decorator
    def post(self,request):
        try:
            data = json.loads(request.body)
            user = request.user
            music_ids  = data['music_id']
            for music_id in music_ids:
                if not MyFavoriteMusic.objects.filter(user = user, music_id = music_id).exists():
                    MyFavoriteMusic.objects.create(user = user, music_id = music_id)
            return HttpResponse(status =200)
        
        except KeyError:
            return JsonResponse({ 'message' : 'INVALID_KEYS' }, status =400)

    @login_decorator
    def get(self,request):
        try:
            user = request.user
            favorite_songs = MyFavoriteMusic.objects.filter(user = user)
            favorite_song_list = []
            for song in favorite_songs:
                artist = []
                music_artists = song.music.musicartist_set.all()
                for music_artist in music_artists:
                    artist.append(music_artist.artist.name)
                favorite_list = {
                    'music_id'  : song.music.id,
                    'music_name': song.music.name,
                    'image'     : song.music.album.image_url,
                    'album_name': song.music.album.name,
                    'artist'    : artist,
                    'lyrics'    : song.music.lyrics,
                    'Is_liked'  : True}
                favorite_song_list.append(favorite_list)
            return JsonResponse({ 'data' : favorite_song_list },status =200)
        
        except KeyError:
            return JsonResponse({ 'message' : 'INVALID_KEYS' },status = 400)



