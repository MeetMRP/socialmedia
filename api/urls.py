from django.urls import path
from .views import LikePost, UnlikePost, MakePost, SentConnect, ViewConnect, UpdateConnectStatus, RecommendConnections

urlpatterns = [
    path('post/', MakePost.as_view(), name='make-post'),
    path('posts/<int:pk>/like/', LikePost.as_view(), name='like-post'),
    path('posts/<int:pk>/unlike/', UnlikePost.as_view(), name='unlike-post'),
    path('send-connect/', SentConnect.as_view(), name='sent-connect'),
    path('connections/', ViewConnect.as_view(), name='sent-connect'),
    path('connections/<int:pk>/status/', UpdateConnectStatus.as_view(), name='update-connection-status'),
    path('recommend-connections/', RecommendConnections.as_view(), name='recommend-connections'),
]
