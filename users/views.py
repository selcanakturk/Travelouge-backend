from rest_framework import generics, permissions, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from travelouge import settings
from users.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import UserRegisterSerializer, UserSerializer
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail


from rest_framework.parsers import MultiPartParser, FormParser

User = get_user_model()

token_generator = PasswordResetTokenGenerator()

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

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

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        old_email = user.email  # Mevcut maili al

        if 'profile_picture' in request.FILES:
            if user.profile_picture:
                user.profile_picture.delete(save=False)

        serializer = UserSerializer(user, data=request.data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            updated_user = serializer.save()

            # E-posta değişmişse kullanıcıya bilgilendirme maili gönder
            if old_email != updated_user.email:
                print(" Email değişikliği algılandı, mail gönderiliyor...")
                send_mail(
                    subject="Your email has been updated",
                    message="Hi! Your email address has just been changed on Travelouge. If this wasn’t you, please contact support.",
                    from_email= settings.EMAIL_HOST_USER,
                    recipient_list=[updated_user.email],
                    fail_silently=False,
                )
                print(" Mail gönderildi.")

            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            return Response({"message": "Eski ve yeni şifre gereklidir."},
                            status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(old_password):
            return Response({"message": "Eski şifre yanlış."},
                            status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Şifre başarıyla değiştirildi."},
                        status=status.HTTP_200_OK)
    
class PublicUserProfileView(RetrieveAPIView):
     queryset = User.objects.all()
     serializer_class = UserSerializer
     permission_classes = [AllowAny]
     lookup_field = 'id'

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    email = request.data.get('email')
    if not email:
        return Response({"error": "Email is required"}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"message": "If the email exists, a reset link will be sent."}, status=200)

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)

    reset_url = f"https://reset-password-ui-91pg.vercel.app/reset-password.html?uid={uid}&token={token}"
    send_mail(
        subject="Password Reset Request",
        message=f"To reset your password, click on the link below:\n{reset_url}",
        from_email="noreply@travelouge.com",
        recipient_list=[user.email],
        fail_silently=False,
    )

    return Response({"message": "If the email exists, a reset link was sent."}, status=200)

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request):
    uidb64 = request.data.get('uid')
    token = request.data.get('token')
    new_password = request.data.get('new_password')

    if not uidb64 or not token or not new_password:
        return Response({"error": "All fields are required"}, status=400)

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        return Response({"error": "Invalid UID"}, status=400)

    if not token_generator.check_token(user, token):
        return Response({"error": "Invalid or expired token"}, status=400)

    user.set_password(new_password)
    user.save()

    return Response({"message": "Password reset successful!"}, status=200)