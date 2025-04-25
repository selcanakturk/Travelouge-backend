from rest_framework import serializers
from routes.models import Route, RouteCoordinate, RouteImage

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
    profile_picture = serializers.SerializerMethodField()  # 🆕

    images = RouteImageSerializer(many=True, read_only=True)
    coordinates = RouteCoordinateSerializer(many=True, read_only=True)

    class Meta:
        model = Route
        fields = [
            'id', 'user', 'username', 'profile_picture',  # 🆕 eklendi
            'title', 'description',
            'created_at', 'is_deleted',
            'images', 'coordinates',
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
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
