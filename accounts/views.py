from django.db import transaction
from base.choices import UserType
from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer
from base.utils import get_jwt_auth_token
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from strings import *
from django.utils import timezone


from django.contrib.auth import authenticate



def response(data=None, message=None, code=status.HTTP_200_OK, extra_data={}):
    result = {'status': {'code': code,
                         'message': message},
              'data': data
              }
    result.update(extra_data)
    return Response(result)


class RegistrationView(APIView):
    permission_classes = (AllowAny,)
    throttle_scope = 'on_boarding'

    @transaction.atomic
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data, context={'request': request, 'view': self})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return response(data=serializer.data, extra_data={'token': get_jwt_auth_token(user)})


class LoginAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = authenticate(
            request,
            username=request.data['email'],
            password=request.data['password']
        )
        if user is None:
            return response(message='CANNOT_LOGIN', code=status.HTTP_401_UNAUTHORIZED)
        CustomUser.objects.filter(id=user.id).update(last_login=timezone.now())
        user_data = CustomUserSerializer(user, context={'request': request}).data
        message = LOGIN_SUCCESS.format(user.first_name)
        return response(data=user_data, message=message, extra_data={'token': get_jwt_auth_token(user)})


class LiveLocationUpdateAPI(APIView):

    @transaction.atomic
    def patch(self, request):
        serializer = CustomUserSerializer(
            instance=self.request.user, data=request.data, context={
                'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return response(data=serializer.data)


class RestaurantListAPIView(GenericAPIView, ListModelMixin):
    queryset = CustomUser.objects.filter(user_type=UserType.restaurant.value[0])
    serializer_class = CustomUserSerializer


    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
