# from app.views import ShortenerCreateApiView,UserCreate,LoginView,Redirector,ShortenerListAPIView,SumurlListAPIView,ShortenerUpdateApiView,ShortenerDeleteApiView,AlbumListAPIView
from app.views import *
from django.urls import path

app_name='api'

urlpatterns = [
    path('showcount/<str:datestart>/<str:dateend>/',CountShortenerListAPIView.as_view(),name='showcount_api'),
    path("users/",UserCreate.as_view(), name="user_create"),
    path("login/", LoginView.as_view(), name="login"),
    path('create/',ShortenerCreateApiView.as_view(),name='create_url'),
    path('showurlid/<int:pk>/',ShortenerCreateApiView.as_view(),name='show_url_id'),
    path('url/<slug:shortener_link>/',Redirector.as_view(),name='redirector'),
    path('showurl/',ShortenerListAPIView.as_view(),name='show_url'),
    path('albumsearch/<int:pk>/',AlbumSearch.as_view(),name='albumsearch'),
    path('sumurl/',SumurlListAPIView.as_view(),name='sum_url'),
    path('update/<str:pk>',ShortenerUpdateApiView.as_view(),name='update_api'),
    path('delete/<str:pk>',ShortenerDeleteApiView.as_view(),name='delete_api'),
    path('showalbum/',AlbumListAPIView.as_view(),name='show_album_py'),
    path('showalbumURL/',AlbumListURLAPIView.as_view(),name='show_albumURL'),
    path('showalbum/<slug:pk>',AlbumListAPIView.as_view(),name='show_album'),
    path('story/<slug:pk>/',StoryAPIView.as_view(),name='story'),
    # path('test/',test.as_view()),
]