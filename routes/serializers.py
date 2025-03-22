from rest_framework import serializers, viewsets, permissions
from django.contrib.auth import get_user_model
from .models import Route, Location, RouteLocation, RouteImage, Comment, Like

User = get_user_model()

# ---- SERIALIZERS ----
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class RouteLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteLocation
        fields = '__all__'

class RouteImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteImage
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Comment
        fields = ['id', 'route', 'user', 'text', 'created_at']

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Like
        fields = ['id', 'route', 'user', 'created_at']

class RouteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    locations = RouteLocationSerializer(many=True, read_only=True)
    images = RouteImageSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Route
        fields = ['id', 'user', 'title', 'description', 'created_at', 'locations', 'images', 'comments', 'likes']
