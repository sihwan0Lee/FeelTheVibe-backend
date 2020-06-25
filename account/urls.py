from django.urls import path
from .views import NaverSocialSignInView, MyFavoriteMusicView

urlpatterns = [
        path('/sign-in', NaverSocialSignInView.as_view()),
        path('/favorite-music',MyFavoriteMusicView.as_view()),
]
