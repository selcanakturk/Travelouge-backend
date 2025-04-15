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

class RouteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    images = RouteImageSerializer(many=True, read_only=True)
    coordinates = RouteCoordinateSerializer(many=True, read_only=True)

    class Meta:
        model = Route
        fields = ['id', 'user', 'title', 'description', 'created_at', 'is_deleted', 'images', 'coordinates']
