from django.urls import path
from .views import NaverSocialSignInView

urlpatterns = [
        path('/sign-in', NaverSocialSignInView.as_view()),
]        
