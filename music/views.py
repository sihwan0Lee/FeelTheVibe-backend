import json

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse

from .models import Music, Album, Artist
from account.models import User, MyPlaylist

class MusicPlayView(View)

    def get(self,request):


