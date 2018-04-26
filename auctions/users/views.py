from rest_framework import status, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserSerializer, AuthUserSerializer


class UserCreateView(APIView):
    """
    Creates the user.
    """

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthTokenView(ObtainAuthToken):
    """
    Sign In API.
    """
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_serializer = AuthUserSerializer(user)
        token, created = Token.objects.get_or_create(user=user)
        print()

        return Response({
            'user': user_serializer.data,
            'token': token.key
        })
