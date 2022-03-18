import json

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status

from basic.utils.validator import is_valid_password
from basic.models import Profile
from basic.utils.serializer import profile_serializer

from backend.decorators import parse_header

@permission_classes((AllowAny,))
class UserViewSet(viewsets.ViewSet):
    http_method_names = ["post", "get"]

    @action(detail=False, methods=['GET'])
    @method_decorator(parse_header())
    def profile(self, request, *args, **kwargs):
        """사용자 정보"""

        user = request.user
        if not user:
            return Response({ 'details': 'Invalid user' }, status=status.HTTP_400_BAD_REQUEST)
        
        profile, created = Profile.objects.get_or_create(user=user, name=user.username)
        data = profile_serializer(profile)
        
        return Response(data, status=status.HTTP_200_OK)
        
        password = request.data.get('password', None)

        if username and password:
            user = User.objects.filter(username=username).first()
            if user: 
                return Response({ 'details': 'Username is already taken.' }, status=status.HTTP_400_BAD_REQUEST)
            is_valid, details = is_valid_password(password)
            if not is_valid:
                return Response({ 'details': details }, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                profile = auth.authenticate(request, username=username, password=password)
                if profile is not None:
                    token, created = Token.objects.get_or_create(user=profile)
                    return Response(headers={ 'token': str(token) }, status=status.HTTP_200_OK)
                else:
                    return Response({ 'details': "Can't create user." }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({ 'details': 'Username and password required.' }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def login(self, request, *args, **kwargs):
        """로그인"""
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if username and password:
            profile = auth.authenticate(request, username=username, password=password)
            if profile is not None:
                token, created = Token.objects.get_or_create(user=profile)
                return Response(headers={ 'token': str(token) }, status=status.HTTP_200_OK)
            else:
                return Response({ 'details': "Invalid Username or Password" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({ 'details': 'Username and Password Required' }, status=status.HTTP_400_BAD_REQUEST)