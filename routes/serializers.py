from rest_framework import serializers
from routes.models import Route, RouteCoordinate, RouteImage
from routes.models import Like, Comment


class RouteImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteImage
        fields = ['id', 'image']


class RouteCoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteCoordinate
        fields = ["latitude", "longitude"]


from rest_framework import serializers

class RouteSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()  
    likes_count = serializers.SerializerMethodField()
    is_liked_by_current_user = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    images = RouteImageSerializer(many=True, read_only=True)
    coordinates = RouteCoordinateSerializer(many=True, read_only=True)

    class Meta:
        model = Route
        fields = [
            'id', 'user', 'username', 'profile_picture',  
            'title', 'description',
            'created_at', 'is_deleted',
            'images', 'coordinates', 'likes_count', 'comments_count',
            'is_liked_by_current_user', 
        ]

    def get_user(self, obj):
        return obj.user.id if obj.user else None

    def get_username(self, obj):
        return obj.user.username if obj.user else "unknown"
    
    def get_profile_picture(self, obj):
     request = self.context.get('request')
     if request and obj.user and obj.user.profile_picture:
        return request.build_absolute_uri(obj.user.profile_picture.url)
     return None
    
    def get_likes_count(self, obj):
        return obj.likes.count()  
    
    def get_is_liked_by_current_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def get_comments_count(self, obj):
        return obj.comments.count()  
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
    

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'route', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'route', 'text', 'created_at', 'username', 'profile_picture']

    def get_username(self, obj):
        return obj.user.username

    def get_profile_picture(self, obj):
        request = self.context.get('request')
        if request and obj.user.profile_picture:
            return request.build_absolute_uri(obj.user.profile_picture.url)
        return None
