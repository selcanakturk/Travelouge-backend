from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture')

    # def get_profile_picture(self, obj):
    #     request = self.context.get('request')
    #     if obj.profile_picture:
    #         url = obj.profile_picture.url
    #         if request is not None:
    #             return request.build_absolute_uri(url)
    #         return url
    #     return None
    
class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Bu alan DB'ye kaydedilmeyecek
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)