import jwt
import json
import requests
import bcrypt

from django.views import View
from django.http  import JsonResponse,HttpResponse
from vibe_main.settings  import SECRET_KEY, HASH
from .models import User

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
                return JsonResponse({"token" : token,"nickname":user.nickname, "image":user.image_url}, status = 200)

            else:
                User(
                    name = user_info['response']["name"],
                    nickname = user_info['response']["nickname"],
                    image_url = user_info['response']["profile_image"],
                    email = user_info['response']["email"]
                    ).save()
                user = User.objects.get(email = user_info['response']['email'])
                token = jwt.encode({"email":user_info['response']['email']}, SECRET_KEY, algorithm = HASH).decode('utf-8')
                return JsonResponse({"message":"SUCCESS"}, status = 200)
        except  KeyError as e:
            return JsonResponse({"message":"INVALID_KEYS"}, status = 400)
