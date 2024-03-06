from django.urls import path
from .views import RegisterAPI, LoginAPI, ProtectedAPIView, UserPatchView

urlpatterns = [
    path('auth/register/', RegisterAPI.as_view(), name='register'),
    path('auth/login/', LoginAPI.as_view(), name='login'),
    path('update-details/', UserPatchView.as_view(), name='user-update'),
    path('protected/', ProtectedAPIView.as_view(), name='protected-api'),
]
