from django.urls import path

from .views import (CustomObtainJSONWebToken, CustomUserProfileApiView, CustomUserCreateAPIView)


urlpatterns = [
    path('api/registration/', CustomUserCreateAPIView.as_view(), name='registration'),
    path('api/profile/', CustomUserProfileApiView.as_view(), name='profile'),
    path('api/token-auth/', CustomObtainJSONWebToken.as_view(), name='obtain-jwt'),
]
