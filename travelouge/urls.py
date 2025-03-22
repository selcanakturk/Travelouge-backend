from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import JsonResponse

def home_view(request):
    return JsonResponse({"message": "Welcome to Travelouge API!"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('routes.urls')),  # routes app'iniz
    path('api/', include('users.urls')),  # users app'iniz

    # JWT Authentication URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Ana sayfa JSON yanıtı
    path('', home_view),
]
