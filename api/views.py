from .models import Post, Like, Connection
from .serializers import PostSerializer, SentConnectSerializer, GetConnectSerializer, UpdateConnectStatusSerializer

from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import User
from accounts.serializers import UserSerializer
from knox.auth import TokenAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# api to make a post
class MakePost(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PostSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

# api to like a post
class LikePost(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk, format=None):
        user = request.user
        post = Post.objects.get(pk=pk)
        if Like.objects.filter(post=post, user=user).exists():
            return Response(data='Post already liked', status=status.HTTP_400_BAD_REQUEST)
        Like.objects.create(post=post, user=user)

        return Response(data='Post liked', status=status.HTTP_201_CREATED)

# api to unlike a post
class UnlikePost(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, pk, format=None):
        user = request.user
        post = Post.objects.get(pk=pk)
        like = Like.objects.filter(post=post, user=user)
        if like.exists():
            like.delete()
            return Response(data='Post unliked', status=status.HTTP_200_OK)

        return Response(data='Post already unliked', status=status.HTTP_404_NOT_FOUND)

# sent connection request
class SentConnect(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SentConnectSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(requester=request.user)

        return Response(data={
            'message': 'Connection request sent',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

# View all connections I am requester/ addressee with a status filter ["accepted", "pending", "rejected"]
class ViewConnect(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GetConnectSerializer

    # Custom swagger docx parameter configurations
    status_param_config = openapi.Parameter(
        name='status', in_=openapi.IN_QUERY, description='enter status ["accepted", "pending", "rejected"]', type=openapi.TYPE_STRING)
    as_param_config = openapi.Parameter(
        name='as_a', in_=openapi.IN_QUERY, description='check as a requester/ addressee', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[status_param_config, as_param_config])
    def get(self, request, *args, **kwargs):
        status = request.query_params.get('status', 'pending')
        as_a = request.query_params.get('as_a', 'addressee')

        if as_a == 'addressee':
            connect_requests = Connection.objects.filter(
                addressee=request.user)
        elif as_a == 'requester':
            connect_requests = Connection.objects.filter(
                requester=request.user)

        if status in ['accepted', 'pending', 'rejected']:
            connect_requests = connect_requests.filter(status=status)

        serializer = GetConnectSerializer(connect_requests, many=True)
        return Response(serializer.data)

# Accept or reject pending requests
class UpdateConnectStatus(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(request_body=UpdateConnectStatusSerializer)
    def put(self, request, pk, format=None):
        try:
            connection = Connection.objects.get(pk=pk, addressee=request.user)
        except Connection.DoesNotExist:
            return Response({'message': 'Connection request not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateConnectStatusSerializer(
            connection, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# recommendation using mutual connections
class RecommendConnections(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user

        # Find all users the current user is connected to
        connected_users = Connection.objects.filter(
            Q(requester=user, status='accepted') | Q(
                addressee=user, status='accepted')
        ).values_list('requester__id', 'addressee__id')

        # Flatten the list and remove duplicates and the user's own id
        connected_user_ids = set(
            [item for sublist in connected_users for item in sublist if item != user.id])
        
        # Find connections of these connections (excluding the user and already connected users)
        recommendations = Connection.objects.filter(
            Q(requester__id__in=connected_user_ids, status='accepted')
        ).exclude(addressee=user).exclude(addressee__id__in=connected_user_ids)
        
        # Extract IDs
        recommended_user_ids_set = set()
        for recommendation in recommendations.values_list('requester__id', 'addressee__id'):
            recommended_user_ids_set.update(recommendation)
        
        # Remove already connected user IDs and the user's own ID
        recommended_user_ids = recommended_user_ids_set - \
            connected_user_ids - {user.id}
        
        # Get user models for the recommended IDs
        recommended_users = User.objects.filter(id__in=recommended_user_ids)
        serializer = UserSerializer(recommended_users, many=True)

        return Response(serializer.data)