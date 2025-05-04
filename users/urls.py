from django.urls import path
from users.views import UserRegisterView, LoginView, UserProfileView, ChangePasswordView, PublicUserProfileView, password_reset_confirm, password_reset_request
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('users/<int:id>/', PublicUserProfileView.as_view(), name='public-user-profile'),
    path('password-reset-request/', password_reset_request),
    path('password-reset-confirm/', password_reset_confirm),


] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
