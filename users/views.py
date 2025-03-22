from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import UserRegisterSerializer, UserSerializer
from django.contrib.auth.hashers import make_password


User = get_user_model()

# Kullanıcı Kaydı için RegisterView sınıfı yerine UserRegisterView kullanılabilir.
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name") 
        #bu işlemler genelde serailizerda ya da services.py dosyasında yapılır. amaç viewi temiz tutmak. 

        # Kullanıcı adı ve e-posta kontrolü
        if User.objects.filter(username=username).exists():
            return Response({"message": "Username already exists!"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"message": "Email already exists!"}, status=status.HTTP_400_BAD_REQUEST)

        # Yeni kullanıcı oluşturulması
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),  # Şifreyi hash'leme
            first_name=first_name,
            last_name=last_name
        )

        return Response({"message": "Registration successful!"}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username
            })
        else:
            return Response({"message": "Invalid credentials!"}, status=status.HTTP_401_UNAUTHORIZED)
        



# Profil Güncelleme için UserProfileView kullanıyoruz
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user  # Sadece oturum açan kullanıcının verisini döndürür

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserSerializer(user, data=request.data, partial=True)  # Kısmi güncelleme
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
