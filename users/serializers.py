from rest_framework import serializers
from django.contrib.auth import get_user_model

# Kullanıcı Modeli
User = get_user_model()

# Kullanıcı Kaydı İçin Serializer
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
#validate fonk gelmesi gerekiyor password içim, change password için kübraya yaz.
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

# Kullanıcı Profil Görüntüleme ve Güncelleme İçin Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

