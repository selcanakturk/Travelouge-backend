from rest_framework import serializers
from .models import Route, RouteImage

class RouteImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteImage
        fields = ['id', 'image']

class RouteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # Kullanıcıyı otomatik al
    images = RouteImageSerializer(many=True, read_only=True)  # Rotaya bağlı tüm resimleri getir

    class Meta:
        model = Route
        fields = ['id', 'user', 'title', 'description', 'images']
