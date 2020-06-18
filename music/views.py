

from django.views import View
from django.http import HttpResponse, JsonResponse

from .models import Music, Album, Artist
from account.models import User, MyPlaylist

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
                artist=[]
                for m in music_artists:
                    artist.append(m.artist.name)
                chart_list={
                    'id'        : chart.id,
                    'image_url' : chart.album.image_url,
                    'name'      : chart.name,
                    'artist'    : artist,
                    'album'     : chart.album.name,
                    'lyrics'    : chart.lyrics,
                    'select'    : False}
                chart100.append(chart_list)
            return JsonResponse({'data' : chart100}, status=200)

class MusicDetailView(View):
    def get(self, request,music_id):
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
