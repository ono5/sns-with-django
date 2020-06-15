from django.shortcuts import render
from rest_framework import generics, authentication, permissions
from api_user import serializers
from core.models import Profile, FriendRequest
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response


class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer


class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = serializers.FriendRequestSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(Q(ask_to=self.request.user) | Q(ask_from=self.request.user))

    # 新規作成をオーバーライド
    def perform_create(self, serializer):
        try:
            serializer.save(ask_from=self.request.user)
        except Exception as e:
            raise ValidationError("User can have only unique request")

    # delete
    def destroy(self, request, *args, **kwargs):
        response = {'message': 'Delete is not allowed!'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # Update
    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'Patch is not allowed!'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
