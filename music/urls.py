from django.urls import path
from .views import MusicCountView, ChartView, MusicDetailView, StreamingView, MyPlaylistView, MyPlaylistDetailView, MusicAddView, MusicDeleteView, PlayerView

urlpatterns = [
    path('/count', MusicCountView.as_view()),
    path('/chart', ChartView.as_view()),
    path('/detail/<int:music_id>', MusicDetailView.as_view()),
    path('/stream', StreamingView.as_view()),
    path('/myplaylist',MyPlaylistView.as_view()),
    path('/myplaylist/<int:myplaylist_id>', MyPlaylistDetailView.as_view()),
    path('/add', MusicAddView.as_view()),
    path('/delete/<int:myplaylist_id>', MusicDeleteView.as_view()),
    path('/player', PlayerView.as_view()),
    ]
