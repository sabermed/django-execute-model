from django.urls import path
from .views import GetVideoResult


urlpatterns = [
  path('get-video-result/', GetVideoResult.as_view(), name="get-video-result"),
]