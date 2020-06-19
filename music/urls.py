from django.urls import path
from .views import MusicCountView, ChartView, MusicDetailView

urlpatterns = [
    path('/count', MusicCountView.as_view()),
    path('/chart', ChartView.as_view()),
    path('/detail/<int:music_id>', MusicDetailView.as_view())
]
