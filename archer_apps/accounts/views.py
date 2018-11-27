from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer

from rest_framework_jwt.views import JSONWebTokenAPIView
from .serializers import CustomJSONWebTokenSerializer


class CustomObtainJSONWebToken(JSONWebTokenAPIView):
    """
        API View that receives a POST with a user's email and password.
        Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = CustomJSONWebTokenSerializer


class CustomUserCreateAPIView(generics.GenericAPIView):
    """
        API call to register new user
        Required fields: email, password
        Not req field: type (journalist, editor)
    """
    permission_classes = (AllowAny, )
    serializer_class = CustomUserSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = request.data.get('email')
            password = request.data.get('password')
            user_type = request.data.get('user_type')
            user = CustomUser.objects.create_user(
                email=email, password=password
            )
            if user_type:
                user.user_type = user_type
                user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserProfileApiView(generics.ListAPIView):
    """
        API call to retrieve current user
    """
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CustomUserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
